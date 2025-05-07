import numpy as np

class Weissberger:
    def __init__(self):
        self.df_values = {
            "forest": 1.0,
            "sparse_forest": 0.5,
            "low_vegetation": 0.25,
            "barren": 0.1,
        }

    def calcular(self, f_GHz, d_km, tipo_vegetacion):
        df = self.df_values.get(tipo_vegetacion.lower(), 0.0)
        d_effective = d_km * df * 1000  # Distancia efectiva de vegetación
        
        if d_effective >= 0.014:  
            return 1.33 * (f_GHz ** 0.284) * (d_effective ** 0.588)
        else:
            return 0.45 * (f_GHz ** 0.284) * d_effective