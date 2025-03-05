# Se importan las bibliotecas necesarias para el procesamiento de datos raster y la visualización.
import rasterio
import matplotlib.pyplot as plt
import numpy as np

# Se carga el archivo reclasificado de Corine Land Cover.
archivo_corine = 'ESA_WorldCoverSanFrancisco_reclassified_to_Corine.tif'  # Se define la ruta del archivo GeoTIFF.
with rasterio.open(archivo_corine) as src:
    corine_map = src.read(1)  # Se lee la primera banda del archivo.

# Se definen colores y etiquetas para las clases de Corine Land Cover.
corine_colors = {
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
    999: ('black', 'Sin datos'),  # Valor para píxeles sin datos
    # Se agregan clases adicionales para valores desconocidos.
    0: ('black', 'Sin datos'),
    55: ('darkred', 'Zona desconocida 55'),  # Color oscuro
    65: ('darkmagenta', 'Zona desconocida 65'),  # Color oscuro
    66: ('darkcyan', 'Zona desconocida 66'),  # Color oscuro
    76: ('darkgray', 'Zona desconocida 76'),  # Color oscuro
    79: ('darkorange', 'Zona desconocida 79'),  # Color oscuro para el valor 79
    155: ('darkbrown', 'Zona desconocida 155')  # Color oscuro
}

# Se verifican los valores únicos presentes en el archivo reclasificado.
valores_unicos = np.unique(corine_map)
print("Valores únicos en el archivo reclasificado:", valores_unicos)

# Se asegura que todos los valores únicos estén en la tabla de colores.
# Si un valor no está en la tabla, se asigna un color oscuro y una etiqueta "Desconocido".
for value in valores_unicos:
    if value not in corine_colors:
        print(f"Advertencia: El valor {value} no está en la tabla de colores.")
        corine_colors[value] = ('darkgray', f'Desconocido ({value})')  # Color oscuro por defecto

# Se crea una imagen con colores personalizados.
corine_image = np.zeros((corine_map.shape[0], corine_map.shape[1], 3), dtype=np.uint8)
for value, (color, _) in corine_colors.items():
    mask = (corine_map == value)  # Se crea una máscara para la categoría actual.
    corine_image[mask] = np.array(plt.cm.colors.to_rgb(color)) * 255  # Se asigna el color correspondiente.

# Se muestra el mapa de Corine Land Cover con una leyenda personalizada.
plt.figure(figsize=(12, 8))
plt.imshow(corine_image)
plt.axis('off')  # Se ocultan los ejes.

# Se crea la leyenda.
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
          for value, (color, label) in corine_colors.items()]
plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left', title='Categorías de Corine Land Cover')

plt.title('Mapa de Corine Land Cover (Reclasificado desde ESA WorldCover)')
plt.show()