import numpy as np

class P1411:
    def __init__(self):
        self.coeficientes = {
            # Debajo de tejado
            "dense_residential": {"alpha": 3.01, "beta": 18.8, "gamma": 2.07, "sigma": 3.07},
            "urban": {"alpha": 5.06, "beta": -4.68, "gamma": 2.02, "sigma": 9.33},
            "dense_urban": {"alpha": 4.00, "beta": 10.2, "gamma": 2.36, "sigma": 7.60},
            "industrial": {"alpha": 2.12, "beta": 29.2, "gamma": 2.11, "sigma": 5.06},
            # Encima de tejado
            "high_buildings": {"alpha": 4.39, "beta": -6.27, "gamma": 2.30, "sigma": 6.89},
            "building_blocks": {"alpha": 2.29, "beta": 28.6, "gamma": 1.96, "sigma": 3.48},
        }

    def calcular(self, f_GHz, distancia_km, entorno):
        coef = self.coeficientes.get(entorno.lower())
        if not coef:
            raise ValueError(f"Entorno no válido. Opciones: {list(self.coeficientes.keys())}")
        return 10 * coef["alpha"] * np.log10(distancia_km * 1000) + coef["beta"] + 10 * coef["gamma"] * np.log10(f_GHz)