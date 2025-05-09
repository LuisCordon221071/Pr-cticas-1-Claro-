# MODELO DE PÉRDIDAS POR PROPAGACIÓN - CLARO PRÁCTICAS

## REQUISITOS
- Python 3.8 o superior
- Bibliotecas requeridas:
  - NumPy

Instalación de dependencias:
pip install numpy

## INSTALACIÓN
1. Clonar el repositorio:
git clone https://github.com/LuisCordon221071/Pr-cticas-1-Claro-.git
cd Pr-cticas-1-Claro-

2. Ejecutar el programa principal:
python main.py

## LÓGICA DE FUNCIONAMIENTO

El programa utiliza tres modelos principales:

1. ITU-R P.1411: Para entornos urbanos (residencial, urbano, industrial)
2. Weissberger: Para pérdidas por vegetación (bosques, vegetación baja)
3. Free Space: Modelo básico con ajustes para agua/terreno abierto

El controlador combina estos modelos para 17 tipos de entornos predefinidos.

## CÓMO USARLO

1. Ejecutar main.py
2. Seleccionar una opción del menú:
   - 1-17 para entornos específicos
   - 18 para tabla completa
3. Ingresar frecuencia (GHz) y distancia (km)
4. Visualizar resultados o exportar a archivo

## EJEMPLOS DE USO

1. Cálculo básico desde código Python:
from controlador import Controlador
calc = Controlador()
result = calc.calcular(1.9, 1.0, 1)  # 1.9 GHz, 1 km, Residencial Denso
print(f"Pérdidas totales: {result['total']:.2f} dB")

2. Desde la interfaz:
- Para zona urbana a 2.1 GHz, 0.5 km:
  Opción: 2
  Frecuencia: 2.1
  Distancia: 0.5

- Para tabla completa a 0.8 GHz, 2 km:
  Opción: 18
  Frecuencia: 0.8
  Distancia: 2.0

## ESTRUCTURA DEL PROYECTO
main.py              # Interfaz de usuario principal
controlador.py       # Lógica central y combinación de modelos
p1411.py             # Modelo ITU-R P.1411
weissberger.py       # Modelo de Weissberger
free_space.py        # Modelo de espacio libre
README.md            # Documentación

## LICENCIA
Este proyecto está bajo la licencia MIT.

## CONTRIBUCIONES
Las contribuciones son bienvenidas. Por favor abrir un issue o pull request para sugerencias.

Desarrollado por Luis Cordón para Claro Guatemala (https://github.com/LuisCordon221071)
