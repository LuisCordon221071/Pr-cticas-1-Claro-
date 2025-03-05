# Se importan las bibliotecas necesarias para el procesamiento de datos raster y la visualización.
import rasterio
import matplotlib.pyplot as plt
import numpy as np

# Se carga el archivo GeoTIFF de ESA WorldCover.
archivo_tif = 'ESA_WorldCover_10m_2021_v200_N36W123_Map.tif'  # Se define la ruta del archivo GeoTIFF.
with rasterio.open(archivo_tif) as src:
    landcover_map = src.read(1)  # Se lee la primera banda del archivo.
    transform = src.transform  # Se guarda la transformación geográfica del archivo.

# Se definen colores y etiquetas para cada categoría de landcover.
landcover_colors = {
    10: ('forestgreen', 'Árboles'),
    20: ('limegreen', 'Arbustos'),
    30: ('gold', 'Praderas'),
    40: ('yellow', 'Cultivos'),
    50: ('red', 'Áreas urbanas'),
    60: ('tan', 'Suelo desnudo'),
    70: ('white', 'Nieve/hielo'),
    80: ('blue', 'Agua'),
    90: ('darkgreen', 'Humedales'),
    95: ('darkblue', 'Manglares'),
    100: ('lightgreen', 'Musgos/líquenes')
}

# Se crea una imagen con colores personalizados.
landcover_image = np.zeros((landcover_map.shape[0], landcover_map.shape[1], 3), dtype=np.uint8)
for value, (color, _) in landcover_colors.items():
    mask = (landcover_map == value)  # Se crea una máscara para la categoría actual.
    landcover_image[mask] = np.array(plt.cm.colors.to_rgb(color)) * 255  # Se asigna el color correspondiente.

# Se muestra el mapa de landcover con una leyenda personalizada.
fig, ax = plt.subplots(figsize=(12, 8))
im = ax.imshow(landcover_image)
plt.axis('off')  # Se ocultan los ejes.

# Se crea la leyenda.
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
          for value, (color, label) in landcover_colors.items()]
plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left', title='Categorías de Landcover')

plt.title('Mapa de Landcover (ESA WorldCover 2020)')

# Se define una función para mostrar coordenadas reales al pasar el mouse.
def mostrar_coordenadas(event):
    if event.inaxes == ax:
        x, y = int(event.xdata), int(event.ydata)
        if 0 <= x < landcover_map.shape[1] and 0 <= y < landcover_map.shape[0]:
            # Se convierten coordenadas de píxeles a coordenadas geográficas.
            lon, lat = transform * (x, y)
            categoria = landcover_map[y, x]
            ax.set_title(f'Coordenadas: ({lon:.4f}, {lat:.4f}) - Categoría: {categoria} ({landcover_colors[categoria][1]})')
            fig.canvas.draw()

# Se conecta la función al evento de movimiento del mouse.
fig.canvas.mpl_connect('motion_notify_event', mostrar_coordenadas)

plt.show()