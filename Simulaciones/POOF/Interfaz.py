class Interfaz:
    def mostrar_menu(self):
        """Muestra el menú principal."""
        print("\n--- Menú Principal ---")
        print("1. Ingresar archivo TIF (ESA o Corine)")
        print("2. Visualizar archivo")
        print("3. Obtener rango de coordenadas válidas")
        print("4. Verificar rango de coordenadas y obtener zonas de clutter")
        print("5. Calcular áreas útiles")
        print("6. Graficar pérdidas vs. distancia")
        print("7. Convertir archivo ESA a Corine")
        print("8. Modificar archivo Corine")
        print("9. Salir")

    def obtener_opcion(self):
        """Obtiene la opción seleccionada por el usuario."""
        return input("Seleccione una opción: ")

    def mostrar_mensaje(self, mensaje):
        """Muestra un mensaje al usuario."""
        print(mensaje)

    def ingresar_ruta(self, mensaje):
        """Solicita al usuario que ingrese una ruta de archivo."""
        return input(mensaje)

    def ingresar_coordenadas(self):
        """Solicita al usuario que ingrese coordenadas."""
        lon = float(input("Ingrese la longitud: "))
        lat = float(input("Ingrese la latitud: "))
        return lon, lat