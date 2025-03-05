# Se importan las bibliotecas necesarias para el cálculo y la visualización.
from pycraf import pathprof, conversions as cnv
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

# Se definen los parámetros de la simulación.
frecuencia = 0.850 * u.GHz  # Se establece la frecuencia de la señal en GHz.
distancias = np.linspace(1, 100, 100) * u.km  # Se crea un arreglo de distancias desde 1 hasta 100 km.

# Se calcula la atenuación por espacio libre para cada distancia.
atenuaciones = cnv.free_space_loss(distancias, frecuencia)

# Se configura y genera la gráfica de los resultados.
plt.figure(figsize=(10, 6))  # Se define el tamaño de la figura.
plt.plot(distancias, atenuaciones, label=f'Frecuencia: {frecuencia}', color='blue')  # Se grafican las distancias vs atenuaciones.
plt.title('Atenuación por espacio libre en el vacío')  # Se añade un título a la gráfica.
plt.xlabel('Distancia (km)')  # Se etiqueta el eje X.
plt.ylabel('Atenuación (dB)')  # Se etiqueta el eje Y.
plt.grid(True)  # Se habilita la cuadrícula en la gráfica.
plt.legend()  # Se muestra la leyenda.
plt.show()  # Se visualiza la gráfica.