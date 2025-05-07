import os
import requests
import zipfile
import numpy as np
import pandas as pd
import geopandas as gpd
from osgeo import gdal, ogr, osr
import matplotlib.pyplot as plt
import rasterio

def get_data():
    url = "https://ftp.wpc.ncep.noaa.gov/shapefiles/fop/fop_20250127.zip"
    download_dir = "/Users/varunsharma/work/Geospatial/SpatialData/eigenrisk"
    zip_path = os.path.join(download_dir, "fop.zip")
    shp_dir = os.path.join(download_dir, "fop")
    os.makedirs(shp_dir, exist_ok=True)
    r = requests.get(url)
    with open(zip_path, "wb") as f:
        f.write(r.content)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(shp_dir)

    for file in os.listdir(shp_dir):
        if file.endswith(".shp"):
            return os.path.join(shp_dir, file)


def add_buffer(shp_path):
    gdf = gpd.read_file(shp_path)
    original_crs = gdf.crs
    utm_crs = gdf.estimate_utm_crs()
    gdf_proj = gdf.to_crs(utm_crs)
    gdf_proj["zone"] = 1
    buffer_2km = gdf_proj.copy()
    buffer_2km["geometry"] = buffer_2km.buffer(2000)
    buffer_2km["zone"] = 2
    buffer_4km = gdf_proj.copy()
    buffer_4km["geometry"] = buffer_4km.buffer(4000)
    buffer_4km["zone"] = 3
    buffer_2km["geometry"] = buffer_2km.geometry.difference(gdf_proj.unary_union)
    buffer_4km["geometry"] = buffer_4km.geometry.difference(buffer_2km.unary_union.union(gdf_proj.unary_union))
    merged = pd.concat([gdf_proj, buffer_2km, buffer_4km])
    merged = merged.to_crs(original_crs)
    merged.to_file("buffered_zones.shp")

    return "buffered_zones.shp"


def rasterize(shp_path):
    out_tif = "zone_raster.tif"
    source_ds = ogr.Open(shp_path)
    layer = source_ds.GetLayer()
    x_min, x_max, y_min, y_max = layer.GetExtent()
    pixel_size = 0.005
    x_res = int((x_max - x_min) / pixel_size)
    y_res = int((y_max - y_min) / pixel_size)
    target_ds = gdal.GetDriverByName('GTiff').Create(out_tif, x_res, y_res, 1, gdal.GDT_Int16, options=["COMPRESS=DEFLATE"])
    target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    target_ds.SetProjection(srs.ExportToWkt())
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(0)
    gdal.RasterizeLayer(target_ds, [1], layer, options=["ATTRIBUTE=zone"])
    target_ds = None
    return out_tif


def remap_tif(input_tif):
    out_tif = "remapped_zones.tif"
    src = gdal.Open(input_tif)
    band = src.GetRasterBand(1)
    array = band.ReadAsArray()
    remap = {1: 100, 2: 50, 3: 25}
    remapped = np.vectorize(remap.get)(array)
    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(out_tif, src.RasterXSize, src.RasterYSize, 1, gdal.GDT_Int16, options=["COMPRESS=DEFLATE"])
    out_ds.SetGeoTransform(src.GetGeoTransform())
    out_ds.SetProjection(src.GetProjection())
    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(remapped)
    out_band.SetNoDataValue(0)
    out_ds = None
    return out_tif

def view_tif(tif_path):
    with rasterio.open(tif_path) as src:
        data = src.read(1)
        plt.imshow(data, cmap='viridis')
        plt.colorbar(label='Zone Value')
        plt.title('Rasterized Zones')
        plt.axis('off')
        plt.show()

def main():
    shp_path = get_data()
    print("Downloaded Shapefile:", shp_path)

    buffered_path = add_buffer(shp_path)
    print("Buffered Zones Shapefile:", buffered_path)

    raster_path = rasterize(buffered_path)
    print("Rasterized Zone TIFF:", raster_path)

    remapped_path = remap_tif(raster_path)
    print("Remapped TIFF Output:", remapped_path)

    view_tif(remapped_path)
    print("TIFF output displayed")

if __name__ == "__main__":
    print("Starting process...")
    main()
    print("Process completed")
