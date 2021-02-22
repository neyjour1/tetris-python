# 2D Tetris python

Tetris simple en python
**interfaz gráfica 2D pygame**

## Setup
1.  clonar el repositorio
2.  `py -m pip install pygame` o `python3 -m pip install pygame`
3.  `py main.py`

## Juego
**inputs**
* Left arrow: mover la pieza a la izquierda 
* Right arrow: mover la pieza a la derecha
* Down arrow: hacer caer la pieza más rápido

### Score
Al limpiar n cantidad de filas (por turno) se aumenta el score de la siguiente forma:
* n=1 fila: 40 puntos
* n=2 filas: 100 puntos
* n=3 filas: 400 puntos
* n=4 filas: 1200 puntos

<strong>como es esperable, por turno solo se pueden limpiar entre 1 y 4 filas, no más ni menos</strong>


