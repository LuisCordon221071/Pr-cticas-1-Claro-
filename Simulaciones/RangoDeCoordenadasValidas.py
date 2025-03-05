# Se importa la biblioteca necesaria para el procesamiento de datos raster.
import rasterio

# Se carga el archivo GeoTIFF.
archivo_clutter = 'ESA_WorldCoverSanFrancisco_reclassified_to_Corine.tif'  # Se define la ruta del archivo GeoTIFF.
with rasterio.open(archivo_clutter) as src:
    # Se obtienen los límites del archivo GeoTIFF.
    bounds = src.bounds
    # Se obtiene el sistema de coordenadas (CRS) del archivo.
    crs = src.crs

# Se muestra el rango de coordenadas aceptable para el archivo GeoTIFF.
print("Rango de coordenadas aceptable para el archivo GeoTIFF:")
print(f"Longitud mínima (Oeste): {bounds.left}")
print(f"Longitud máxima (Este): {bounds.right}")
print(f"Latitud mínima (Sur): {bounds.bottom}")
print(f"Latitud máxima (Norte): {bounds.top}")
print(f"Sistema de coordenadas (CRS): {crs}")