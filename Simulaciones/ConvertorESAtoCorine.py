# Se importan las bibliotecas necesarias para el procesamiento de datos raster.
import rasterio
import numpy as np

# Se carga el archivo GeoTIFF de ESA WorldCover.
archivo_esa = 'ESA_WorldCover_10m_2021_v200_N36W123_Map.tif'  # Se define la ruta del archivo GeoTIFF.
with rasterio.open(archivo_esa) as src:
    esa_map = src.read(1)  # Se lee la primera banda del archivo.
    profile = src.profile  # Se guarda el perfil del archivo (metadatos).

# Se define la tabla de reclasificación de ESA WorldCover a Corine Land Cover.
reclass_table = {
    10: 311,  # Árboles -> Bosques de hoja ancha
    20: 322,  # Arbustos -> Matorrales
    30: 321,  # Praderas -> Pastizales naturales
    40: 211,  # Cultivos -> Tierras de cultivo no irrigadas
    50: 111,  # Áreas urbanas -> Tejido urbano continuo
    60: 332,  # Suelo desnudo -> Rocas desnudas
    70: 335,  # Nieve/hielo -> Glaciares y nieves perpetuas
    80: 512,  # Agua -> Masas de agua
    90: 411,  # Humedales -> Marismas interiores
    95: 421,  # Manglares -> Marismas salinas
    100: 322  # Musgos/líquenes -> Matorrales
}

# Se crea un mapa vacío para almacenar los valores reclasificados.
corine_map = np.zeros_like(esa_map, dtype=np.int16)

# Se aplica la reclasificación utilizando la tabla definida.
for esa_value, corine_value in reclass_table.items():
    corine_map[esa_map == esa_value] = corine_value

# Se guarda el archivo reclasificado como un nuevo GeoTIFF.
archivo_corine = 'ESA_WorldCoverSanFrancisco_reclassified_to_Corine.tif'
with rasterio.open(archivo_corine, 'w', **profile) as dst:
    dst.write(corine_map, 1)  # Se escribe la banda reclasificada en el nuevo archivo.

# Se imprime un mensaje indicando que el archivo ha sido guardado.
print(f"Archivo reclasificado guardado como: {archivo_corine}")