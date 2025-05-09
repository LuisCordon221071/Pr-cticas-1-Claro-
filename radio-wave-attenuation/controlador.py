from p1411 import P1411
from weissberger import Weissberger
from free_space import FreeSpace
import numpy as np

class Controlador:
    def __init__(self):
        self.p1411 = P1411()
        self.weissberger = Weissberger()
        self.free_space = FreeSpace()
        
        self.clutters = {
            # Urbanos (P.1411)
            1: {"nombre": "Residencial Denso", "modelo": "p1411", "tipo": "dense_residential"},
            2: {"nombre": "Urbano", "modelo": "p1411", "tipo": "urban"},
            3: {"nombre": "Urbano Denso", "modelo": "p1411", "tipo": "dense_urban"},
            4: {"nombre": "Manzanas de edificios", "modelo": "p1411", "tipo": "building_blocks"},
            5: {"nombre": "Edificios altos", "modelo": "p1411", "tipo": "high_buildings"},
            6: {"nombre": "Industrial", "modelo": "p1411", "tipo": "industrial"},
            # Vegetación (Weissberger)
            7: {"nombre": "Bosque denso", "modelo": "weissberger", "tipo": "forest"},
            8: {"nombre": "Bosque disperso", "modelo": "weissberger", "tipo": "sparse_forest"},
            9: {"nombre": "Vegetación baja", "modelo": "weissberger", "tipo": "low_vegetation"},
            10: {"nombre": "Terreno árido", "modelo": "weissberger", "tipo": "barren"},
            # Free Space
            11: {"nombre": "Agua interior", "modelo": "free_space", "tipo": "inland"},
            12: {"nombre": "Mar abierto", "modelo": "free_space", "tipo": "sea"},
            13: {"nombre": "Espacio urbano abierto", "modelo": "free_space", "tipo": "urban"},
            # Clutter combinados
            14: {"nombre": "Residencial con árboles", "modelo": "combo", 
                 "componentes": [
                     {"modelo": "p1411", "tipo": "dense_residential"},
                     {"modelo": "weissberger", "tipo": "sparse_forest"}
                 ]},
            15: {"nombre": "Residencial con pocos árboles", "modelo": "combo",
                 "componentes": [
                     {"modelo": "p1411", "tipo": "dense_residential"},
                     {"modelo": "weissberger", "tipo": "low_vegetation"}
                 ]},
            16: {"nombre": "Pueblo", "modelo": "combo",
                 "componentes": [
                     {"modelo": "p1411", "tipo": "urban"},
                     {"modelo": "weissberger", "tipo": "sparse_forest"}
                 ]},
            17: {"nombre": "Humedal", "modelo": "combo",
                 "componentes": [
                     {"modelo": "free_space", "tipo": "inland"},
                     {"modelo": "weissberger", "tipo": "sparse_forest"}
                 ]}
        }

    def calcular_modelo(self, f_GHz, d_km, modelo, tipo):
        """Calcula pérdidas para un modelo específico"""
        if modelo == "p1411":
            return self.p1411.calcular(f_GHz, d_km, tipo)
        elif modelo == "weissberger":
            return self.weissberger.calcular(f_GHz, d_km, tipo)
        elif modelo == "free_space":
            return self.free_space.calcular(f_GHz, d_km) + self.free_space.aplicar_ajuste(tipo)
        return 0

    def calcular(self, f_GHz, d_km, opcion_clutter):
        if opcion_clutter not in self.clutters:
            raise ValueError("Opción de clutter no válida")
        
        clutter = self.clutters[opcion_clutter]
        L_free = self.free_space.calcular(f_GHz, d_km)
        resultados = {
            "nombre": clutter["nombre"],
            "free_space": L_free,
            "componentes": [],
            "total": L_free
        }

        if clutter["modelo"] == "combo":
            # Para modelos combinados
            total_combinado = 0  
            for componente in clutter["componentes"]:
                L_componente = self.calcular_modelo(
                    f_GHz, d_km, 
                    componente["modelo"], 
                    componente["tipo"]
                )
                resultados["componentes"].append({
                    "modelo": componente["modelo"],
                    "tipo": componente["tipo"],
                    "perdidas": L_componente - L_free 
                })
                total_combinado += (L_componente - L_free)
            
            L_clutter = total_combinado / len(resultados["componentes"])
            resultados["total"] += L_clutter
            resultados["promedio_combinado"] = L_clutter

        else:
            # Para modelos individuales
            if clutter["modelo"] == "p1411":
                L_clutter = self.p1411.calcular(f_GHz, d_km, clutter["tipo"])
            elif clutter["modelo"] == "weissberger":
                L_clutter = self.weissberger.calcular(f_GHz, d_km, clutter["tipo"])
            else:  # free_space
                L_clutter = 0
            
            resultados["componentes"].append({
                "modelo": clutter["modelo"],
                "tipo": clutter["tipo"],
                "perdidas": L_clutter - L_free if clutter["modelo"] != "free_space" else 0
            })
            
            if clutter["modelo"] == "free_space":
                ajuste = self.free_space.aplicar_ajuste(clutter["tipo"])
                resultados["total"] += ajuste
                resultados["ajuste"] = ajuste
            else:
                resultados["total"] += L_clutter - L_free

        return resultados
