import math

def calcular_perdida_clutter():
    # Categorías de clutter (obstrucciones) basadas en ITU-R P.452-16 Tabla 4
    categorias_clutter = [
        {"nombre": "Campos de cultivo alto", "h_a": 4, "d_k": 0.1},
        {"nombre": "Zonas de parque", "h_a": 4, "d_k": 0.1},
        {"nombre": "Centro de pueblo", "h_a": 5, "d_k": 0.07},
        {"nombre": "Árboles caducifolios (regular)", "h_a": 15, "d_k": 0.05},
        {"nombre": "Bosque de coníferas (irregular)", "h_a": 20, "d_k": 0.05},
        {"nombre": "Bosque tropical", "h_a": 20, "d_k": 0.03},
        {"nombre": "Zona suburbana", "h_a": 9, "d_k": 0.025},
        {"nombre": "Suburbano denso", "h_a": 12, "d_k": 0.02},
        {"nombre": "Urbano", "h_a": 20, "d_k": 0.02},
        {"nombre": "Urbano denso", "h_a": 25, "d_k": 0.02},
        {"nombre": "Urbano con rascacielos", "h_a": 35, "d_k": 0.02},
        {"nombre": "Zona industrial", "h_a": 20, "d_k": 0.05}
    ]
    
    # Mostrar opciones de clutter
    print("\nOpciones de categorías de clutter (obstrucciones):")
    for i, categoria in enumerate(categorias_clutter, start=1):
        print(f"{i}. {categoria['nombre']}")
    
    # Solicitar entrada del usuario
    try:
        seleccion = int(input("\nSeleccione el tipo de clutter (número): "))
        if seleccion < 1 or seleccion > len(categorias_clutter):
            raise ValueError
    except ValueError:
        print("¡Entrada inválida! Por favor ingrese un número de la lista.")
        return
    
    frecuencia = float(input("Ingrese la frecuencia (GHz, ej. 2.0 para 2 GHz): "))
    if frecuencia < 0.1 or frecuencia > 100:
        print("La frecuencia debe estar entre 0.1 GHz y 100 GHz.")
        return
    
    h_a = categorias_clutter[seleccion-1]["h_a"]
    d_k = categorias_clutter[seleccion-1]["d_k"]
    
    # Altura de la antena (opcional)
    h = input(f"Ingrese la altura de la antena (m) [por defecto={h_a}]: ")
    h = float(h) if h.strip() else h_a
    
    # Paso 1: Calcular factor de frecuencia (F_fc)
    F_fc = 0.25 + 0.375 * (1 + math.tanh(7.5 * (frecuencia - 0.5)))
    
    # Paso 2: Calcular pérdida por clutter (A_h)
    tanh_arg = 6 * (h / h_a - 0.625)
    A_h = 10.25 * F_fc * math.exp(-d_k) * (1 - math.tanh(tanh_arg)) - 0.33
    
    # Ajustar pérdida entre 5 dB y 20 dB (según ITU-R P.452-16)
    min_perdida = 5.0 if frecuencia >= 0.1 else 0.0
    if frecuencia >= 0.9:
        max_perdida = 20.0
    else:
        max_perdida = min_perdida + (frecuencia - 0.1) * (20 - 5) / 0.8
    A_h_ajustada = max(min_perdida, min(A_h, max_perdida))
    
    # Mostrar resultados
    print("\n--- Resultados ---")
    print(f"Categoría de clutter: {categorias_clutter[seleccion-1]['nombre']}")
    print(f"Altura nominal del clutter (h_a): {h_a} m")
    print(f"Distancia nominal del clutter (d_k): {d_k} km")
    print(f"Frecuencia: {frecuencia} GHz")
    print(f"Altura de la antena: {h} m")
    print(f"Pérdida por clutter (sin ajustar): {A_h:.2f} dB")
    print(f"Pérdida por clutter (ajustada según ITU-R): {A_h_ajustada:.2f} dB")

# Ejecutar el programa
if __name__ == "__main__":
    calcular_perdida_clutter()