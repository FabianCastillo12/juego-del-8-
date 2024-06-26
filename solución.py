from queue import PriorityQueue
import copy

# Estado inicial del tablero
board = [
    [5, 8, 6],
    [0, 4, 7],
    [2, 3, 1],
]

# Estado objetivo del tablero
board_solved = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
]
solved_moves = {}
count = 0 # número de nodos
initial = copy.deepcopy(board)  # representa el estado inicial del tablero
board_previous = copy.deepcopy(board)   # representa el tablero antes de realizar un movimiento derecha/izquierda/arriba/abajo

# Verifica si el tablero es resoluble
def is_solvable(board):
    flat_board = [num for row in board for num in row if num != 0]  
    inversions = sum(1 for i in range(len(flat_board) - 1) for j in range(i + 1, len(flat_board)) if flat_board[i] > flat_board[j])
    return inversions % 2 == 0

# Realiza un seguimiento inverso desde el nodo objetivo hasta el nodo inicial
def backtrack(n1):
    current = n1
    g_score = 0
    solved = current == board_solved

    while not solved or current != came_from["previous_node0"]:
        if solved:
             # Guarda los movimientos en el diccionario solved_moves
            solved_moves["move%s" % g_score] = current
            for x in current:
                print(x)
            print("\n")
            if current == initial:
                print(str(g_score) + " movimientos \n")

        for i in range(0, len(nodes.keys())):
            if nodes["node%s" % i] == current:
                current = came_from["previous_node%s" % i]
                g_score += 1
                if solved:
                    solved_moves["move%s" % g_score] = current
                if current == came_from["previous_node0"]:
                    return g_score
                break

# Calcula la distancia de Manhattan entre el estado actual y el objetivo
def distance():   
    man = 0
    for i in range(1,9):
        x1, y1 = find(board, i)
        x2, y2 = find(board_solved, i)
        distance = abs(x2 - x1) + abs(y2 - y1)
        man += distance
    return man

# Restricciones para moverse a la derecha o izquierda
def RLrestrict():
    global allow_r, allow_l
    allow_r = all(board[i][2] != 0 for i in range(3))
    allow_l = all(board[i][0] != 0 for i in range(3))

# Restricciones para moverse hacia arriba o abajo
def UDrestrict():
    global allow_u, allow_d
    allow_u = all(board[0][i] != 0 for i in range(3))
    allow_d = all(board[2][i] != 0 for i in range(3))

# Encuentra la fila y columna de un número en el tablero
def find(board, num):   
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == num:
                return (i, j)  # row, col

# Mueve la ficha vacía a la derecha intercambiándola con el número a su izquierda
def right():   
    i, j = find(board, 0)
    board[i][j], board[i][j + 1] = board[i][j + 1], board[i][j]
    return board

# Mueve la ficha vacía hacia arriba intercambiándola con el número debajo de ella
def up():   
    i, j = find(board, 0)
    board[i][j], board[i-1][j] = board[i-1][j], board[i][j]
    return board

# Mueve la ficha vacía a la izquierda intercambiándola con el número a su derecha
def left():   
    i, j = find(board, 0)
    board[i][j], board[i][j - 1] = board[i][j - 1], board[i][j]
    return board

# Mueve la ficha vacía hacia abajo intercambiándola con el número encima de ella
def down():  
    i, j = find(board, 0)
    board[i][j], board[i + 1][j] = board[i + 1][j], board[i][j]
    return board

# Representa un nodo con atributos: posición, f_score
class Node:   
    def __init__(self, position, f_score):
        self.position = position
        self.f_score = f_score  #allows storing more data into a single variable for ease


def in_closed(n1):   # Verifica si un nodo ya ha sido explorado
    if len(closed_set) == 1:    
        return False
    if n1 == closed_set["start"]:
        return True
    if n1 in closed_set.values():
        return True
    return False


n1 = Node(board, distance())  
open_set = PriorityQueue()  # prioridad
nodes = {}   
closed_set = {}  # nodos explorados
came_from = {}   
closed_set["start"] = copy.deepcopy(board)  

if is_solvable(board):
    print("Buscando... \n")
    while board != board_solved:  
        RLrestrict()
        UDrestrict()
        if allow_r:       # si se puede mover a la derecha
            n1.position = right()    # el tablero se mueve a la derecha, y el estado del tablero se guarda en el atributo de posición de n1
            if in_closed(n1.position):  # comprueba si el nodo fue explorado antes
                left()    # si el nodo fue explorado anteriormente, no se volverá a explorar y el tablero volverá al estado anterior
            if not in_closed(n1.position):     # si el nodo no fue explorado
                nodes["node%s" % count] = n1.position   # el nodo se agrega al diccionario de nodos totales
                came_from["previous_node%s" % count] = copy.deepcopy(left())   # se agrega el nodo anterior al diccionario
                n1.position = copy.deepcopy(right())  
                h_score = distance()  # calcula la puntuación h del nodo explorado
                n1.f_score = h_score + backtrack(n1.position)   # puntuación h + puntuación g = puntuación f
                open_set.put((n1.f_score, h_score, count, n1.position))  # los valores se colocan en la cola
                board = copy.deepcopy(board_previous)  # el tablero retrocede 1 movimiento
                count += 1   
        if allow_l:  
            n1.position = left()
            if in_closed(n1.position):
                right()
            if not in_closed(n1.position):
                nodes["node%s" % count] = n1.position
                came_from["previous_node%s" % count] = copy.deepcopy(right())
                n1.position = copy.deepcopy(left())
                h_score = distance()
                n1.f_score = h_score + backtrack(n1.position)
                open_set.put((n1.f_score, h_score, count, n1.position))
                board = copy.deepcopy(board_previous)
                count += 1
        if allow_u:
            n1.position = up()
            if in_closed(n1.position):
                down()
            if not in_closed(n1.position):
                nodes["node%s" % count] = n1.position
                came_from["previous_node%s" % count] = copy.deepcopy(down())
                n1.position = copy.deepcopy(up())
                h_score = distance()
                n1.f_score = h_score + backtrack(n1.position)
                open_set.put((n1.f_score, h_score, count, n1.position))
                board = copy.deepcopy(board_previous)
                count += 1
        if allow_d:
            n1.position = down()
            if in_closed(n1.position):
                up()
            if not in_closed(n1.position):
                nodes["node%s" % count] = n1.position
                came_from["previous_node%s" % count] = copy.deepcopy(up())
                n1.position = copy.deepcopy(down())
                h_score = distance()
                n1.f_score = h_score + backtrack(n1.position)
                open_set.put((n1.f_score, h_score, count, n1.position))
                board = copy.deepcopy(board_previous)
                count += 1

        next_item = open_set.get()[3]   
        board = copy.deepcopy(next_item)   
        if board == board_solved:
            print("RESUELTO")
            break
        closed_set["node%s" %count] = copy.deepcopy(next_item)  
        board_previous = copy.deepcopy(board)  

else:
    print("No se puede resolver")

print(str(len(closed_set)) + " nodos explorados")
print(str(len(nodes)) + " total de nodos")





