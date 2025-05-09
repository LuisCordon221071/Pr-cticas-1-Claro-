from controlador import Controlador
from datetime import datetime

def mostrar_menu_principal():
    print("\nMODELOS DE PROPAGACION - MENU PRINCIPAL")
    print("--------------------------------------")
    print("Seleccione el tipo de entorno/clutter:")
    print("\nUrbanos (P.1411):")
    print(" 1. Residencial Denso")
    print(" 2. Urbano")
    print(" 3. Urbano Denso")
    print(" 4. Manzanas de edificios")
    print(" 5. Edificios altos")
    print(" 6. Industrial")
    
    print("\nVegetacion (Weissberger):")
    print(" 7. Bosque denso")
    print(" 8. Bosque disperso")
    print(" 9. Vegetacion baja")
    print("10. Terreno arido")
    
    print("\nFree Space:")
    print("11. Agua interior")
    print("12. Mar abierto")
    print("13. Espacio urbano abierto")
    
    print("\nEntornos combinados:")
    print("14. Residencial con arboles")
    print("15. Residencial con pocos arboles")
    print("16. Pueblo")
    print("17. Humedal")

    print("\n18. Ver tabla con perdidas para todos los entornos")
    print(" 0. Salir")

def mostrar_resultados(resultado):
    print(f"\nRESULTADOS PARA: {resultado['nombre']}")
    print("-" * 40)
    print(f"Perdidas por espacio libre: {resultado['free_space']:.2f} dB")
    
    for i, comp in enumerate(resultado['componentes'], 1):
        print(f"\nComponente {i}:")
        print(f"   Modelo: {comp['modelo'].upper()}")
        print(f"   Tipo: {comp['tipo']}")
        print(f"   Perdidas adicionales: {comp['perdidas']:.2f} dB")
    
    if 'ajuste' in resultado:
        print(f"\nAjuste adicional: {resultado['ajuste']:.2f} dB")
    
    print("\n" + "=" * 40)
    print(f"PERDIDAS TOTALES: {resultado['total']:.2f} dB")
    print("=" * 40)

def mostrar_tabla_perdidas(calculadora, f_GHz, d_km):
    print("\nTABLA DE PERDIDAS POR ENTORNO")
    print("-" * 50)
    print(f"Frecuencia: {f_GHz:.2f} GHz")
    print(f"Distancia: {d_km:.2f} km")
    free_space = calculadora.free_space.calcular(f_GHz, d_km)
    print(f"Perdidas en espacio libre: {free_space:.2f} dB")
    print("-" * 50)
    print(f"{'Entorno':<30} {'Adicionales (dB)':>20} {'Totales (dB)':>20}")
    print("-" * 70)

    tabla_lineas = []

    for i in range(1, 18):
        resultado = calculadora.calcular(f_GHz, d_km, i)
        nombre = resultado["nombre"]

        if "ajuste" in resultado:
            adicionales = resultado["ajuste"]
        else:
            # Si hay más de un componente, es un entorno combinado
            componentes = resultado["componentes"]
            adicionales = sum(comp["perdidas"] for comp in componentes)
            if len(componentes) > 1:
                adicionales /= len(componentes)

        total = resultado["total"]
        print(f"{nombre:<30} {adicionales:>20.2f} {total:>20.2f}")
        tabla_lineas.append((nombre, adicionales, total))


    return tabla_lineas, free_space

def guardar_tabla_en_txt(tabla_lineas, f_GHz, d_km, free_space):
    nombre_archivo = f"tabla_perdidas_{f_GHz:.2f}GHz.txt".replace('.', '_')
    try:
        with open(nombre_archivo, 'w') as f:
            f.write(f"TABLA DE PERDIDAS POR ENTORNO\n")
            f.write(f"Frecuencia: {f_GHz:.2f} GHz\n")
            f.write(f"Distancia: {d_km:.2f} km\n")
            f.write(f"Perdidas en espacio libre: {free_space:.2f} dB\n\n")
            f.write(f"{'Entorno':<30} {'Adicionales (dB)':>20} {'Totales (dB)':>20}\n")
            f.write("-" * 70 + "\n")
            for nombre, adicionales, total in tabla_lineas:
                f.write(f"{nombre:<30} {adicionales:>20.2f} {total:>20.2f}\n")
        print(f"\nTabla guardada en '{nombre_archivo}'")
    except Exception as e:
        print(f"Error al guardar: {str(e)}")

def main():
    print("Sistema de calculo de perdidas por propagacion")
    print("---------------------------------------------")
    calculadora = Controlador()
    
    while True:
        mostrar_menu_principal()
        try:
            opcion = input("\nSeleccione una opcion (0-18): ").strip()
            
            if opcion == '0':
                print("\nFin del programa")
                break
                
            if not opcion.isdigit() or int(opcion) not in range(0, 19):
                print("Error: Ingrese un numero entre 0 y 18")
                continue
                
            opcion = int(opcion)
            
            print("\nParametros de simulacion:")
            try:
                f_GHz = float(input("   Frecuencia (GHz): "))
                d_km = float(input("   Distancia (km): "))
                
                if f_GHz <= 0 or d_km <= 0:
                    print("Error: Valores deben ser positivos")
                    continue
                    
            except ValueError:
                print("Error: Ingrese valores numericos validos")
                continue
            
            if opcion == 18:
                tabla, free_space = mostrar_tabla_perdidas(calculadora, f_GHz, d_km)
                exportar = input("\n¿Desea exportar esta tabla a archivo? (s/n): ").lower()
                if exportar == 's':
                    guardar_tabla_en_txt(tabla, f_GHz, d_km, free_space)
                continue
            
            resultado = calculadora.calcular(f_GHz, d_km, opcion)
            mostrar_resultados(resultado)
            
            exportar = input("\nExportar resultados a archivo? (s/n): ").lower()
            if exportar == 's':
                try:
                    with open('resultados_propagacion.txt', 'a') as f:
                        f.write(f"\n{'='*50}\n")
                        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Configuracion: {resultado['nombre']}\n")
                        f.write(f"Frecuencia: {f_GHz} GHz | Distancia: {d_km} km\n")
                        f.write(f"Perdidas totales: {resultado['total']:.2f} dB\n")
                    print("Resultados exportados a 'resultados_propagacion.txt'")
                except Exception as e:
                    print(f"Error al exportar: {str(e)}")
                    
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            print("Intente nuevamente")

if __name__ == "__main__":
    main()
