from ArchivoTIF import ArchivoTIF
from Coordenadas import Coordenadas
from Graficas import Graficas
from Interfaz import Interfaz
from astropy import units as u

class Controlador:
    def __init__(self):
        self.interfaz = Interfaz()
        self.archivo_tif = None
        self.coordenadas = None
        self.graficas = Graficas()

    def ejecutar(self):
        """Ejecuta el programa."""
        while True:
            self.interfaz.mostrar_menu()
            opcion = self.interfaz.obtener_opcion()

            if opcion == "1":
                self.ingresar_archivo_tif()
            elif opcion == "2":
                self.visualizar_archivo()
            elif opcion == "3":
                self.obtener_rango_coordenadas()
            elif opcion == "4":
                self.verificar_rango_coordenadas()
            elif opcion == "5":
                self.calcular_areas_utiles()
            elif opcion == "6":
                self.graficar_perdidas_vs_distancia()
            elif opcion == "7":
                self.convertir_esa_a_corine()
            elif opcion == "8":
                self.modificar_corine()
            elif opcion == "9":
                self.interfaz.mostrar_mensaje("Saliendo del programa...")
                break
            else:
                self.interfaz.mostrar_mensaje("Opción no válida. Intente de nuevo.")

    def ingresar_archivo_tif(self):
        """Permite al usuario ingresar un archivo TIF."""
        ruta = input("Ingrese la ruta del archivo TIF: ")
        self.archivo_tif = ArchivoTIF(ruta)
        self.archivo_tif.cargar_archivo()
        self.coordenadas = Coordenadas(self.archivo_tif)
        self.interfaz.mostrar_mensaje("Archivo TIF cargado correctamente.")

    def visualizar_archivo(self):
        """Visualiza el archivo TIF."""
        if self.archivo_tif:
            self.archivo_tif.visualizar_archivo()
        else:
            self.interfaz.mostrar_mensaje("Error: No se ha cargado ningún archivo.")

    def obtener_rango_coordenadas(self):
        """Obtiene el rango de coordenadas válidas."""
        if self.coordenadas:
            self.coordenadas.obtener_rango_coordenadas()
        else:
            self.interfaz.mostrar_mensaje("Error: No se ha cargado ningún archivo.")

    def verificar_rango_coordenadas(self):
        """Verifica si las coordenadas están dentro del rango válido y obtiene la zona de clutter."""
        if self.coordenadas:
            # Coordenadas del transmisor
            lon_t = float(input("Ingrese la longitud del transmisor: "))
            lat_t = float(input("Ingrese la latitud del transmisor: "))

            # Coordenadas del receptor
            lon_r = float(input("Ingrese la longitud del receptor: "))
            lat_r = float(input("Ingrese la latitud del receptor: "))

            # Verificar rango de coordenadas
            transmisor_dentro = self.coordenadas.verificar_rango_coordenadas(lon_t, lat_t)
            receptor_dentro = self.coordenadas.verificar_rango_coordenadas(lon_r, lat_r)

            # Obtener zonas de clutter
            zona_t = self.coordenadas.obtener_zona_clutter(lon_t, lat_t)
            zona_r = self.coordenadas.obtener_zona_clutter(lon_r, lat_r)

            # Mostrar resultados
            print("\nResultados:")
            print(f"Transmisor ({lon_t}, {lat_t}): {'Dentro' if transmisor_dentro else 'Fuera'}")
            print(f"Receptor ({lon_r}, {lat_r}): {'Dentro' if receptor_dentro else 'Fuera'}")

            if zona_t is not None:
                print(f"Zona de clutter del transmisor: {zona_t} ({self.archivo_tif.corine_colors.get(zona_t, ('Desconocido', 'Desconocido'))[1]})")
            else:
                print("Zona de clutter del transmisor: Fuera de los límites del archivo.")

            if zona_r is not None:
                print(f"Zona de clutter del receptor: {zona_r} ({self.archivo_tif.corine_colors.get(zona_r, ('Desconocido', 'Desconocido'))[1]})")
            else:
                print("Zona de clutter del receptor: Fuera de los límites del archivo.")
        else:
            self.interfaz.mostrar_mensaje("Error: No se ha cargado ningún archivo.")

    def calcular_areas_utiles(self):
        """Calcula las áreas útiles."""
        if self.archivo_tif:
            self.archivo_tif.calcular_areas_utiles()
        else:
            self.interfaz.mostrar_mensaje("Error: No se ha cargado ningún archivo.")

    def graficar_perdidas_vs_distancia(self):
        """Grafica las pérdidas vs. la distancia."""
        if self.archivo_tif:
            # Definir coordenadas del transmisor y receptor
            lon_t = float(input("Ingrese la longitud del transmisor: ")) * u.deg
            lat_t = float(input("Ingrese la latitud del transmisor: ")) * u.deg
            lon_r = float(input("Ingrese la longitud del receptor: ")) * u.deg
            lat_r = float(input("Ingrese la latitud del receptor: ")) * u.deg

            self.graficas.graficar_perdidas_vs_distancia(self.archivo_tif, lon_t, lat_t, lon_r, lat_r)
        else:
            self.interfaz.mostrar_mensaje("Error: No se ha cargado ningún archivo.")

    def convertir_esa_a_corine(self):
        """Convierte un archivo ESA WorldCover a Corine Land Cover."""
        if self.archivo_tif:
            ruta_salida = self.interfaz.ingresar_ruta("Ingrese la ruta de salida para el archivo Corine: ")
            ruta_corine = self.archivo_tif.convertir_esa_a_corine(ruta_salida)
            self.archivo_tif = ArchivoTIF(ruta_corine)
            self.archivo_tif.cargar_archivo()
            self.interfaz.mostrar_mensaje(f"Archivo Corine guardado en: {ruta_corine}")
        else:
            self.interfaz.mostrar_mensaje("Error: No se ha cargado ningún archivo ESA.")

    def modificar_corine(self):
        """Modifica el archivo Corine Land Cover para incluir categorías adicionales."""
        if self.archivo_tif:
            ruta_salida = self.interfaz.ingresar_ruta("Ingrese la ruta de salida para el archivo Corine modificado: ")
            ruta_modificada = self.archivo_tif.modificar_corine(ruta_salida)
            self.archivo_tif = ArchivoTIF(ruta_modificada)
            self.archivo_tif.cargar_archivo()
            self.interfaz.mostrar_mensaje(f"Archivo Corine modificado guardado en: {ruta_modificada}")
        else:
            self.interfaz.mostrar_mensaje("Error: No se ha cargado ningún archivo Corine.")