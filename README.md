# noaa_buffer_zone_rasterizer

# NOAA Buffer Zones Rasterizer

This Python utility automates the process of downloading NOAA Forecast of Precipitation (FOP) shapefiles, creating buffer zones around the forecast polygons, rasterizing those zones, and remapping zone values for further analysis or visualization.

## 📦 Features

- 📥 **Automatic download** of NOAA FOP shapefiles
- 📏 **Geospatial buffering** at 2km and 4km around input polygons
- 🗺️ **Rasterization** of vector buffers into GeoTIFF
- 🔁 **Remapping** zone values (e.g., core = 100, 2km buffer = 50, 4km buffer = 25)
- 📊 **Visualization** using `rasterio` and `matplotlib`

## 🗂️ Folder Structure

project/ ├── main.py ├── buffered_zones.shp ├── zone_raster.tif ├── remapped_zones.tif └── README.md


## 🛠️ Requirements

- Python 3.8+
- [GDAL](https://gdal.org/)
- [GeoPandas](https://geopandas.org/)
- [Rasterio](https://rasterio.readthedocs.io/)
- NumPy
- Matplotlib
- Requests

Install them via:

```bash
pip install geopandas rasterio numpy matplotlib requests


## 🛠️ Requirements

- Python 3.8+
- [GDAL](https://gdal.org/)
- [GeoPandas](https://geopandas.org/)
- [Rasterio](https://rasterio.readthedocs.io/)
- NumPy
- Matplotlib
- Requests

Install them via:

```bash
pip install geopandas rasterio numpy matplotlib requests
