# Se importan las bibliotecas necesarias para el procesamiento de datos raster y la visualización.
import rasterio
import matplotlib.pyplot as plt
import numpy as np

# Se carga el archivo reclasificado de Corine Land Cover.
archivo_corine = 'ESA_WorldCoverSanFrancisco_reclassified_to_Corine.tif'  # Se define la ruta del archivo GeoTIFF.
with rasterio.open(archivo_corine) as src:
    corine_map = src.read(1)  # Se lee la primera banda del archivo.

# Se definen colores y etiquetas para las clases de Corine Land Cover presentes.
corine_colors = {
    111: ('red', 'Tejido urbano continuo'),          # Áreas urbanas (ESA 50)
    211: ('yellowgreen', 'Tierras de cultivo no irrigadas'),  # Cultivos (ESA 40)
    311: ('darkgreen', 'Bosques de hoja ancha'),     # Árboles (ESA 10)
    321: ('lightgreen', 'Pastizales naturales'),     # Praderas (ESA 30)
    322: ('khaki', 'Matorrales'),                    # Arbustos (ESA 20), Musgos/líquenes (ESA 100)
    332: ('lightgray', 'Rocas desnudas'),            # Suelo desnudo (ESA 60)
    335: ('white', 'Glaciares y nieves perpetuas'),  # Nieve/hielo (ESA 70)
    411: ('lightblue', 'Marismas interiores'),       # Humedales (ESA 90)
    421: ('darkblue', 'Marismas salinas'),           # Manglares (ESA 95)
    512: ('blue', 'Masas de agua')                   # Agua (ESA 80)
}

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