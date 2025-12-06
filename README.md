# 🎮 Puzzle 8 Solver

Una aplicación de escritorio moderna para resolver el clásico **Puzzle 8** (8-puzzle) utilizando el algoritmo **A\*** con heurística de distancia de Manhattan.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Descripción

El Puzzle 8 es un rompecabezas deslizante que consiste en un marco de 3×3 con 8 fichas numeradas y un espacio vacío. El objetivo es reorganizar las fichas desde un estado inicial hasta alcanzar un estado objetivo específico.

Esta aplicación implementa una solución óptima utilizando el algoritmo de búsqueda A\* con la heurística de distancia de Manhattan, garantizando el menor número de movimientos posibles.

## ✨ Características

- 🚀 **Solución Óptima**: Encuentra el camino más corto usando A\*
- 🎨 **Interfaz Moderna**: Diseño dark mode con colores vibrantes
- 📊 **Estadísticas Detalladas**: Nodos explorados, generados, eficiencia y tiempo
- ▶️ **Navegación Paso a Paso**: Visualiza la solución movimiento por movimiento
- ✏️ **Editor de Estados**: Personaliza los estados inicial y objetivo
- ✅ **Validación Matemática**: Verifica si un puzzle tiene solución
- 🏗️ **Arquitectura Modular**: Lógica separada de la interfaz

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8 o superior
- Tkinter (incluido con Python en la mayoría de instalaciones)

### Instalación

1. **Clona el repositorio**:

```bash
git clone https://github.com/tuusuario/juego-del-8.git
cd juego-del-8
```

2. **Ejecuta la aplicación**:

```bash
python main.py
```

¡Eso es todo! No se requieren dependencias externas.

## 📖 Uso

1. **Resolver Puzzle**: Haz clic en el botón "🚀 Resolver Puzzle" para encontrar la solución óptima
2. **Navegar Solución**: Usa los botones "◀ Anterior" y "Siguiente ▶" para ver cada paso
3. **Editar Estados**: Personaliza los estados inicial y objetivo con el botón "✏️ Editar Estados"
4. **Reiniciar**: Vuelve al estado inicial con el botón "🔄 Reiniciar"

### Ejemplo de Estados

**Estado Inicial Predeterminado**:

```
6 5 1
2 8 7
3 4 ·
```

**Estado Objetivo**:

```
1 2 3
4 5 6
7 8 ·
```

## 🏗️ Estructura del Proyecto

```
juego-del-8/
├── main.py                    # Punto de entrada de la aplicación
├── puzzle_solver.py           # Lógica del algoritmo A*
├── puzzle_gui.py              # Interfaz gráfica (Tkinter)
├── README.md                  # Este archivo
└── DIAGRAMA DE ESTADOS.pdf    # Documentación adicional
```

### Módulos

#### `puzzle_solver.py`

Módulo de lógica pura con el algoritmo A\*:

- `a_star(start, goal)` - Implementación del algoritmo A\*
- `manhattan_distance(state, goal)` - Función heurística
- `is_solvable(board)` - Validación de resolubilidad
- `get_neighbors(state)` - Generación de estados vecinos

#### `puzzle_gui.py`

Módulo de interfaz gráfica:

- `PuzzleGUI` - Clase principal de la interfaz
- Visualización del tablero en canvas
- Controles interactivos
- Estadísticas en tiempo real

#### `main.py`

Punto de entrada simple que inicializa la aplicación.

## 🧮 Algoritmo

### A\* (A-star)

El algoritmo A\* es un algoritmo de búsqueda informada que encuentra el camino más corto entre dos nodos. Utiliza una función de evaluación:

```
f(n) = g(n) + h(n)
```

Donde:

- `g(n)` = Costo desde el inicio hasta el nodo actual
- `h(n)` = Estimación heurística desde el nodo actual hasta el objetivo
- `f(n)` = Costo total estimado

### Heurística: Distancia de Manhattan

Calcula la suma de las distancias absolutas entre la posición actual y la posición objetivo de cada ficha:

```python
distance = Σ |x_actual - x_objetivo| + |y_actual - y_objetivo|
```

Esta heurística es **admisible** (nunca sobreestima) y **consistente**, garantizando una solución óptima.

### Validación de Resolubilidad

No todos los estados del Puzzle 8 tienen solución. Un puzzle es resoluble si y solo si el número de **inversiones** es par. Una inversión ocurre cuando una ficha mayor aparece antes que una menor en la representación lineal del tablero.

## 📊 Estadísticas

La aplicación muestra:

- **Movimientos Óptimos**: Número mínimo de pasos para resolver
- **Nodos Explorados**: Cantidad de estados examinados
- **Nodos Generados**: Cantidad total de estados creados
- **Eficiencia**: Relación explorados/generados (%)
- **Tiempo de Ejecución**: Duración del algoritmo en segundos

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
