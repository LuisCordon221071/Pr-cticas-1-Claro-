from pycraf import pathprof
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from pyproj import Geod


class Graficas:
    def graficar_perdidas_vs_distancia(self, archivo_tif, lon_t, lat_t, lon_r, lat_r):
        """Grafica las pérdidas de señal en función de la distancia."""
        if archivo_tif.datos is None:
            print("Error: No se ha cargado ningún archivo.")
            return

        # Convertir las zonas de Corine a tipos de clutter P.452
        p452_clutter_zones = pathprof.landcover_to_p452_clutter_zones(
            archivo_tif.datos, pathprof.CORINE_TO_P452_CLASSES
        )

        # Definir coordenadas del transmisor y receptor
        geod = Geod(ellps='WGS84')
        azimut, _, distancia_maxima = geod.inv(lon_t.value, lat_t.value, lon_r.value, lat_r.value)
        distancia_maxima = distancia_maxima * u.m

        # Parámetros para el cálculo de propagación
        frequency = 0.85 * u.GHz  # Frecuencia de la señal
        temperature = 310. * u.K  # Temperatura en Kelvin
        pressure = 980 * u.hPa    # Presión atmosférica
        h_tg, h_rg = 20 * u.m, 30 * u.m  # Alturas del transmisor y receptor
        hprof_step = 100 * u.m  # Resolución del perfil de altura
        time_percent = 0.1 * u.percent  # Porcentaje de tiempo

        # Calcular pérdidas de propagación a lo largo de la ruta
        distancias = np.linspace(0.1, 3, 10) * u.km  # Distancias entre 0.1 y 3 km
        perdidas = []  # Para almacenar las pérdidas de propagación

        for distancia in distancias:
            # Ajustar hprof_step si la distancia es muy pequeña
            if distancia < 5 * hprof_step:
                hprof_step_temp = distancia / 5
            else:
                hprof_step_temp = hprof_step

            # Calcular coordenadas intermedias
            lon_r_temp, lat_r_temp, _ = geod.fwd(lon_t.value, lat_t.value, azimut, distancia.to(u.m).value)
            lon_r_temp *= u.deg
            lat_r_temp *= u.deg

            # Obtener la zona de clutter en la ubicación temporal del receptor
            zone_r_temp = self.obtener_zona_clutter(lon_r_temp.value, lat_r_temp.value, p452_clutter_zones, archivo_tif.transform)

            try:
                # Calcular las pérdidas de propagación
                results = pathprof.losses_complete(
                    frequency,
                    temperature,
                    pressure,
                    lon_t, lat_t,
                    lon_r_temp, lat_r_temp,
                    h_tg, h_rg,
                    hprof_step_temp,
                    time_percent,
                    zone_t=self.obtener_zona_clutter(lon_t.value, lat_t.value, p452_clutter_zones, archivo_tif.transform),
                    zone_r=zone_r_temp,
                )
                perdidas.append(results['L_b'].value)  # Extraer las pérdidas básicas (L_b)
            except Exception as e:
                print(f"Error en la iteración de distancia {distancia}: {e}")
                continue

        # Graficar las pérdidas
        if len(perdidas) == len(distancias):
            plt.figure(figsize=(10, 6))
            plt.plot(distancias, perdidas, label='Pérdidas vs. Distancia', color='blue')
            plt.title('Atenuación vs. Distancia')
            plt.xlabel('Distancia (km)')
            plt.ylabel('Atenuación (dB)')
            plt.grid(True)
            plt.legend()
            plt.show()
        else:
            print(f"Error: las longitudes de distancias y pérdidas no coinciden. Distancias: {len(distancias)}, Pérdidas: {len(perdidas)}")

    def obtener_zona_clutter(self, lon, lat, clutter_zones, transform):
        """Obtiene la zona de clutter para unas coordenadas específicas."""
        x, y = ~transform * (lon, lat)
        x, y = int(x), int(y)
        if 0 <= y < clutter_zones.shape[0] and 0 <= x < clutter_zones.shape[1]:
            return clutter_zones[y, x]
        else:
            return None