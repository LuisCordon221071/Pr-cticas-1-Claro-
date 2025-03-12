import numpy as np
from pyproj import Geod

class Coordenadas:
    def __init__(self, archivo_tif):
        self.archivo_tif = archivo_tif
        self.geod = Geod(ellps='WGS84')

    def obtener_rango_coordenadas(self):
        """Muestra el rango de coordenadas válidas."""
        if self.archivo_tif.bounds is None:
            print("Error: No se ha cargado ningún archivo.")
            return

        print("Rango de coordenadas aceptable para el archivo GeoTIFF:")
        print(f"Longitud mínima (Oeste): {self.archivo_tif.bounds.left}")
        print(f"Longitud máxima (Este): {self.archivo_tif.bounds.right}")
        print(f"Latitud mínima (Sur): {self.archivo_tif.bounds.bottom}")
        print(f"Latitud máxima (Norte): {self.archivo_tif.bounds.top}")

    def verificar_rango_coordenadas(self, lon, lat):
        """Verifica si las coordenadas están dentro del rango válido."""
        if self.archivo_tif.bounds is None:
            print("Error: No se ha cargado ningún archivo.")
            return False

        return (self.archivo_tif.bounds.left <= lon <= self.archivo_tif.bounds.right) and \
               (self.archivo_tif.bounds.bottom <= lat <= self.archivo_tif.bounds.top)

    def obtener_zona_clutter(self, lon, lat):
        """Obtiene la zona de clutter para unas coordenadas específicas."""
        if self.archivo_tif.datos is None or self.archivo_tif.transform is None:
            print("Error: No se ha cargado ningún archivo.")
            return None

        # Convertir coordenadas geográficas a píxeles
        x, y = ~self.archivo_tif.transform * (lon, lat)
        x, y = int(x), int(y)

        # Verificar si las coordenadas están dentro de los límites de la imagen
        if 0 <= y < self.archivo_tif.datos.shape[0] and 0 <= x < self.archivo_tif.datos.shape[1]:
            return self.archivo_tif.datos[y, x]  # Obtener el valor de la zona de clutter
        else:
            return None  # Fuera de los límites de la imagen