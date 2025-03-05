# Se importan las bibliotecas necesarias para el procesamiento de datos raster, cálculos geodésicos y manejo de unidades.
import rasterio
from pyproj import Geod
import numpy as np
from astropy import units as u

# Se carga el archivo GeoTIFF de zonas de clutter.
archivo_clutter = 'ESA_WorldCoverSanFrancisco_reclassified_to_Corine.tif'  # Se define la ruta del archivo GeoTIFF.
with rasterio.open(archivo_clutter) as src:
    clutter_zones = src.read(1)  # Se lee la primera banda del archivo.
    transform = src.transform  # Se obtiene la transformación geográfica del archivo.
    bounds = src.bounds  # Se obtienen los límites del archivo GeoTIFF.

# Se define una función para verificar si las coordenadas están dentro de los límites del archivo.
def coordenadas_dentro_de_limites(lon, lat, bounds):
    return (bounds.left <= lon <= bounds.right) and (bounds.bottom <= lat <= bounds.top)

# Se define una función para obtener la zona de clutter en una ubicación específica.
def obtener_zona_clutter(lon, lat, clutter_zones, transform):
    x, y = ~transform * (lon, lat)  # Se convierten las coordenadas geográficas a píxeles.
    x, y = int(x), int(y)
    if 0 <= y < clutter_zones.shape[0] and 0 <= x < clutter_zones.shape[1]:
        return clutter_zones[y, x]  # Se obtiene la zona de clutter.
    else:
        return None  # Se retorna None si las coordenadas están fuera de los límites de la imagen.

# Se definen las coordenadas del transmisor y receptor.
lon_t, lat_t = -120.5 * u.deg, 36.85 * u.deg  # Coordenadas del transmisor.
lon_r, lat_r = -121.50 * u.deg, 36.50 * u.deg  # Coordenadas del receptor.

# Se calcula el azimut y la distancia entre el transmisor y el receptor.
geod = Geod(ellps='WGS84')
azimut, _, _ = geod.inv(lon_t.value, lat_t.value, lon_r.value, lat_r.value)

# Se verifica si las coordenadas del transmisor y receptor están dentro de los límites del archivo.
print("Verificación de coordenadas:")
print(f"Transmisor ({lon_t}, {lat_t}): {'Dentro' if coordenadas_dentro_de_limites(lon_t.value, lat_t.value, bounds) else 'Fuera'}")
print(f"Receptor ({lon_r}, {lat_r}): {'Dentro' if coordenadas_dentro_de_limites(lon_r.value, lat_r.value, bounds) else 'Fuera'}")

# Se obtienen las zonas de clutter para el transmisor y receptor.
zone_t = obtener_zona_clutter(lon_t.value, lat_t.value, clutter_zones, transform)
zone_r = obtener_zona_clutter(lon_r.value, lat_r.value, clutter_zones, transform)

print("\nZonas de clutter:")
print(f"Zona del transmisor: {zone_t}")
print(f"Zona del receptor: {zone_r}")

# Se verifican coordenadas intermedias y se obtienen las zonas de clutter.
distancias = np.linspace(0.1, 10, 10) * u.km  # Se definen distancias entre 0.1 y 10 km.

print("\nVerificación de coordenadas intermedias y zonas de clutter:")
for distancia in distancias:
    # Se calculan las coordenadas intermedias.
    lon_r_temp, lat_r_temp, _ = geod.fwd(lon_t.value, lat_t.value, azimut, distancia.to(u.m).value)
    dentro = coordenadas_dentro_de_limites(lon_r_temp, lat_r_temp, bounds)
    
    # Se obtiene la zona de clutter en la ubicación temporal del receptor.
    zone_r_temp = obtener_zona_clutter(lon_r_temp, lat_r_temp, clutter_zones, transform)
    
    # Se muestra la información.
    print(f"Distancia: {distancia:.2f}, Coordenadas: ({lon_r_temp:.4f}, {lat_r_temp:.4f}), Dentro: {'Sí' if dentro else 'No'}, Zona de clutter: {zone_r_temp}")