import rasterio
import matplotlib.pyplot as plt
import numpy as np
import rasterio

class ArchivoTIF:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.datos = None
        self.transform = None
        self.bounds = None
        self.corine_colors = {
            111: ('red', 'Tejido urbano continuo'),
            211: ('yellowgreen', 'Tierras de cultivo no irrigadas'),
            311: ('darkgreen', 'Bosques de hoja ancha'),
            321: ('lightgreen', 'Pastizales naturales'),
            322: ('khaki', 'Matorrales'),
            332: ('lightgray', 'Rocas desnudas'),
            335: ('white', 'Glaciares y nieves perpetuas'),
            411: ('lightblue', 'Marismas interiores'),
            421: ('darkblue', 'Marismas salinas'),
            512: ('blue', 'Masas de agua'),
            999: ('black', 'Sin datos'),
            0: ('darkblue', 'Masas de Agua'),
            55: ('darkred', 'Zona desconocida 55'),
            65: ('darkmagenta', 'Zona desconocida 65'),
            66: ('darkcyan', 'Zona desconocida 66'),
            76: ('darkgray', 'Zona desconocida 76'),
            79: ('darkorange', 'Zona desconocida 79'),
            155: ('saddlebrown', 'Zona desconocida 155')  # Cambiado a 'saddlebrown'
        }

    def cargar_archivo(self):
        """Carga el archivo TIF."""
        with rasterio.open(self.ruta_archivo) as src:
            self.datos = src.read(1)
            self.transform = src.transform
            self.bounds = src.bounds

    def visualizar_archivo(self):
        """Visualiza el archivo TIF con colores personalizados."""
        if self.datos is None:
            print("Error: No se ha cargado ningún archivo.")
            return

        # Verificar valores únicos y asignar colores
        valores_unicos = np.unique(self.datos)
        for value in valores_unicos:
            if value not in self.corine_colors:
                self.corine_colors[value] = ('darkgray', f'Desconocido ({value})')

        # Crear imagen con colores personalizados
        corine_image = np.zeros((self.datos.shape[0], self.datos.shape[1], 3), dtype=np.uint8)
        for value, (color, _) in self.corine_colors.items():
            mask = (self.datos == value)
            try:
                corine_image[mask] = np.array(plt.cm.colors.to_rgb(color)) * 255
            except ValueError:
                print(f"Advertencia: El color '{color}' no es válido. Usando 'darkgray' en su lugar.")
                corine_image[mask] = np.array(plt.cm.colors.to_rgb('darkgray')) * 255

        # Mostrar el mapa
        plt.figure(figsize=(12, 8))
        plt.imshow(corine_image)
        plt.axis('off')

        # Crear leyenda
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
                  for value, (color, label) in self.corine_colors.items()]
        plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left', title='Categorías de Corine Land Cover')

        plt.title('Mapa de Corine Land Cover')
        plt.show()


    def calcular_areas_utiles(self):
        """Calcula el área de cada categoría en el archivo TIF."""
        if self.datos is None:
            print("Error: No se ha cargado ningún archivo.")
            return

        # Obtener la resolución espacial (tamaño de cada píxel en metros)
        with rasterio.open(self.ruta_archivo) as src:
            res_x, res_y = src.res  # Resolución en metros (x, y)

        # Calcular el área de cada píxel en metros cuadrados
        area_pixel = abs(res_x * res_y)

        # Contar píxeles por categoría y calcular áreas
        valores_unicos, conteos = np.unique(self.datos, return_counts=True)
        areas = {value: conteos[i] * area_pixel for i, value in enumerate(valores_unicos)}

        # Mostrar resultados
        print("\nÁreas útiles por categoría (en metros cuadrados):")
        for value, area in areas.items():
            nombre_categoria = self.corine_colors.get(value, ("Desconocido", f"Categoría {value}"))[1]
            print(f"{nombre_categoria}: {area:.2f} m²")

    def convertir_esa_a_corine(self, ruta_salida):
        """Convierte un archivo ESA WorldCover a Corine Land Cover."""
        # Tabla de reclasificación de ESA a Corine
        reclass_table = {
            10: 311,  # Tree cover -> Bosques de hoja ancha
            20: 322,  # Shrubland -> Matorrales
            30: 321,  # Grassland -> Pastizales naturales
            40: 211,  # Cropland -> Tierras de cultivo no irrigadas
            50: 111,  # Built-up -> Tejido urbano continuo
            60: 332,  # Bare / sparse vegetation -> Rocas desnudas
            70: 335,  # Snow and ice -> Glaciares y nieves perpetuas
            80: 512,  # Permanent water bodies -> Masas de agua
            90: 411,  # Herbaceous wetland -> Marismas interiores
            95: 421,  # Mangroves -> Marismas salinas
            100: 322, # Moss and lichen -> Matorrales
            0: 512    # Masas de agua -> Masas de agua
        }

        # Cargar archivo ESA WorldCover
        with rasterio.open(self.ruta_archivo) as src:
            esa_map = src.read(1)
            profile = src.profile

        # Crear un mapa vacío para almacenar los valores reclasificados
        corine_map = np.zeros_like(esa_map, dtype=np.int16)

        # Aplicar la reclasificación
        for esa_value, corine_value in reclass_table.items():
            corine_map[esa_map == esa_value] = corine_value

        # Guardar el archivo reclasificado
        with rasterio.open(ruta_salida, 'w', **profile) as dst:
            dst.write(corine_map, 1)

        print(f"Archivo reclasificado guardado como: {ruta_salida}")
        return ruta_salida

    def modificar_corine(self, ruta_salida):
        """Modifica el archivo Corine Land Cover para incluir categorías adicionales."""
        # Tabla de mapeo para categorías adicionales
        mapeo_adicional = {
            55: 311,  # Tree cover -> Bosques de hoja ancha
            65: 211,  # Cropland -> Tierras de cultivo no irrigadas
            66: 322,  # Shrubland -> Matorrales
            76: 421,  # Mangroves -> Marismas salinas
            155: 411  # Herbaceous wetland -> Marismas interiores
        }

        # Cargar archivo Corine Land Cover
        with rasterio.open(self.ruta_archivo) as src:
            corine_map = src.read(1)
            profile = src.profile

        # Cambiar el tipo de dato a int16 para evitar problemas con valores grandes
        corine_map = corine_map.astype(np.int16)

        # Aplicar el mapeo adicional
        for valor_original, valor_corine in mapeo_adicional.items():
            corine_map[corine_map == valor_original] = valor_corine

        # Actualizar el perfil del archivo para usar int16
        profile.update(dtype=np.int16)

        # Guardar el archivo modificado
        with rasterio.open(ruta_salida, 'w', **profile) as dst:
            dst.write(corine_map, 1)

        print(f"Archivo Corine modificado guardado como: {ruta_salida}")
        return ruta_salida

