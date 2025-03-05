import rasterio
from pycraf import pathprof
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from pyproj import Geod

# Configuración para descargar automáticamente los archivos de altura de terreno faltantes
pathprof.SrtmConf.set(download='missing')

# 1. Cargar el archivo GeoTIFF de zonas de clutter reclasificado
archivo_clutter = 'ESA_WorldCoverLosAngeles_reclassified_to_Corine.tif'  # Reemplaza con la ruta de tu archivo
with rasterio.open(archivo_clutter) as src:
    corine_map = src.read(1)  # Leer la primera banda
    transform = src.transform  # Transformación geográfica del archivo

# 2. Convertir las zonas de Corine a P.452 clutter types
p452_clutter_zones = pathprof.landcover_to_p452_clutter_zones(
    corine_map, pathprof.CORINE_TO_P452_CLASSES
)

# 3. Definir las coordenadas del transmisor y receptor
lon_t, lat_t = -120.56 * u.deg, 37.45 * u.deg  # Transmisor 
lon_r, lat_r = -121.55 * u.deg,  38.5* u.deg  # Receptor

# 4. Obtener las zonas de clutter para el transmisor y receptor
def obtener_zona_clutter(lon, lat, clutter_zones, transform):
    # Convertir coordenadas geográficas a píxeles
    x, y = ~transform * (lon, lat)  # ~transform es la inversa de la transformación
    x, y = int(x), int(y)
    return clutter_zones[y, x]  # Obtener la zona de clutter en las coordenadas

zone_t = obtener_zona_clutter(lon_t.value, lat_t.value, p452_clutter_zones, transform)
zone_r = obtener_zona_clutter(lon_r.value, lat_r.value, p452_clutter_zones, transform)

# 5. Calcular la distancia real entre el transmisor y el receptor
geod = Geod(ellps='WGS84')
azimut, _, distancia_maxima = geod.inv(lon_t.value, lat_t.value, lon_r.value, lat_r.value)
distancia_maxima = distancia_maxima * u.m  # Convertir a unidades de Astropy

# 6. Parámetros para el cálculo de propagación
frequency = 0.85 * u.GHz  # Frecuencia de la señal
temperature = 310. * u.K  # Temperatura en Kelvin
pressure = 980 * u.hPa    # Presión atmosférica
h_tg, h_rg = 20 * u.m, 30 * u.m  # Alturas del transmisor y receptor
hprof_step = 100 * u.m  # Resolución del perfil de altura
time_percent = 0.1 * u.percent  # Porcentaje de tiempo

# 7. Calcular las pérdidas de propagación a lo largo de la ruta
distancias = np.linspace(0.1, 3, 10) * u.km  # Distancias entre 0.1 y 3 km
perdidas = []  # Para almacenar las pérdidas de propagación

for distancia in distancias:
    # Ajustar hprof_step si la distancia es muy pequeña
    if distancia < 5 * hprof_step:
        hprof_step_temp = distancia / 5  # Asegurar al menos 5 puntos
    else:
        hprof_step_temp = hprof_step

    # Calcular las coordenadas intermedias
    lon_r_temp, lat_r_temp, _ = geod.fwd(lon_t.value, lat_t.value, azimut, distancia.to(u.m).value)
    lon_r_temp *= u.deg
    lat_r_temp *= u.deg

    # Obtener la zona de clutter en la ubicación temporal del receptor
    zone_r_temp = obtener_zona_clutter(lon_r_temp.value, lat_r_temp.value, p452_clutter_zones, transform)

    try:
        # Calcular las pérdidas de propagación
        results = pathprof.losses_complete(
            frequency,
            temperature,
            pressure,
            lon_t, lat_t,
            lon_r_temp, lat_r_temp,
            h_tg, h_rg,
            hprof_step_temp,  # Usar el paso ajustado
            time_percent,
            zone_t=zone_t, zone_r=zone_r_temp,
        )
        perdidas.append(results['L_b'].value)  # Extraer las pérdidas básicas (L_b)
    except AssertionError as e:
        print(f"Error en la iteración de distancia {distancia}: {e}")
        continue  # Continuar con la siguiente iteración
    except Exception as e:
        print(f"Error desconocido en la iteración de distancia {distancia}: {e}")
        continue  # Continuar con la siguiente iteración

# 8. Graficar las pérdidas
if len(perdidas) == len(distancias):
    # Graficar las pérdidas
    plt.figure(figsize=(10, 6))
    plt.plot(distancias, perdidas, label=f'Frecuencia: {frequency}', color='blue')
    plt.title('Atenuación vs. Distancia (Prueba Simplificada)')
    plt.xlabel('Distancia (km)')
    plt.ylabel('Atenuación (dB)')
    plt.grid(True)
    plt.legend()
    plt.show()
else:
    print(f"Error: las longitudes de distancias y perdidas no coinciden. Distancias: {len(distancias)}, Pérdidas: {len(perdidas)}")