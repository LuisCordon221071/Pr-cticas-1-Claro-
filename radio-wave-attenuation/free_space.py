import numpy as np

class FreeSpace:
    def __init__(self):
        self.ajustes = {
            "inland": 10,
            "sea": 10,
            "urban": 0,
        }

    def calcular(self, f_GHz, d_km):
        """Pérdidas en espacio libre (modelo básico)"""
        return 20 * np.log10(d_km) + 20 * np.log10(f_GHz) + 32.45

    def aplicar_ajuste(self, entorno_libre):
        return self.ajustes.get(entorno_libre.lower(), 0)