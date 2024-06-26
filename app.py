import pygame
import time
from queue import PriorityQueue
import copy

pygame.init()   # Iniciar pygame

# Carga de imágenes y configuración de la ventana
background_image = pygame.image.load('cubico.jpg')    # Cargar imagen
background_image = pygame.transform.scale(background_image, (1000, 600))

imagen_cuadro = pygame.image.load('images_roca.jpg')
imagen_cuadro = pygame.transform.scale(imagen_cuadro, (193, 193))

win = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Solución de Puzzle 3x3")

# Diccionario de colores y configuración de colores específicos
color_dict = {
    1: (255, 0, 0),     # Rojo
    2: (0, 0, 255),     # Azul
    3: (255, 255, 0),   # Amarillo
    4: (255, 0, 255),   # Magenta
    5: (255, 165, 0),   # Naranja
    6: (0, 128, 0),     # Verde
    7: (128, 128, 128), # Gris 
    8: (128, 0, 128),   # Morado 
    9: (0, 0, 0)        # Negro
}

line_color = (192, 192, 192) # Color de las letras
line_color2 = (0, 255, 255)  # Color celeste fosforescente números

line_width = 20
width = 185
height = 185
vel = 2  # Velocidad de movimientos

default_font = pygame.font.Font('fonts/faster_stroker/Faster Stroker.otf', 80)
default_font2 = pygame.font.Font('fonts/faster_stroker/Faster Stroker.otf', 35)

solved_moves = {}

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

positions = {}
total_moves = 0
initial = copy.deepcopy(board)

class Button:
    def __init__(self, color, x, y, width, height, font_size, text='',  image=None, visible=True, corner_radius=10):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.visible = visible
        self.corner_radius = corner_radius

    def draw(self, win, outline=None):  # Lineas de separación entre botones
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), border_radius=self.corner_radius)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), border_radius=self.corner_radius)
   
        if self.text != '':   # Centrar texto de botones
            button_font = pygame.font.Font('fonts/faster_stroker/Faster Stroker.otf', self.font_size)   #Fuente de los botones
            text = button_font.render(self.text, True, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):  # Verifica clic en boton
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False

# Tamaño de letra botones
button1 = Button((144, 238, 144), 675, 110, 250, 100, 40, "Resolver", corner_radius=20) 
button2 = Button((144, 238, 144), 675, 270, 250, 100, 40, "Reiniciar", corner_radius=20 )

def show_score():   # Muestra total de movimientos
    score = default_font2.render("Movimientos: " + str(total_moves), True, color_dict[1])
    win.blit(score, (645, 435))

def find_nums(board): # Traslada los números en la variable 'board' a las posiciones de los números en el tablero del programa
    for n in range(0,9):
        for i in range(len(board)):  
            for j in range(len(board[0])): 
                if board[i][j] == n:
                    if i == 0:
                        positions["y%s" %n] = 7   
                    if i == 1:
                        positions["y%s" %n] = 205
                    if i == 2:
                        positions["y%s" %n] = 403
                    if j == 0:
                        positions["x%s" %n] = 7  
                    if j == 1:
                        positions["x%s" %n] = 205
                    if j == 2:
                        positions["x%s" %n] = 403

def translate_board():  # Traslada los números en el tablero del programa a la variable 'board'
    for n in range(0,9):
        if positions["y%s" %n] == 7:
            i = 0
        if positions["y%s" %n] == 205:
            i = 1
        if positions["y%s" %n] == 403:
            i = 2
        if positions["x%s" %n] == 7:
            j = 0
        if positions["x%s" %n] == 205:
            j = 1
        if positions["x%s" %n] == 403:
            j = 2
        board[i][j] = n
        find_nums(board)  

# Dibuja la cuadrícula del tablero
def grid():
    pygame.draw.rect(win, color_dict[9], (3, 3, 594, 594), border_radius=10)
    for y in range(3, 600, 198): # Dibujar líneas horizontales
        pygame.draw.line(win, line_color, (0, y), (598, y), line_width)

    for x in range(3, 600, 198): # Dibujar líneas verticales
        pygame.draw.line(win, line_color, (x, 0), (x, 600), line_width)

# Redibuja la ventana con el tablero actualizado
def redraw_window():
    win.blit(background_image, (500, 0))
    grid()

    for n in range(1, 9):
        pygame.draw.rect(win, color_dict[n], (positions[f"x{n}"], positions[f"y{n}"], width, height))
        num = default_font.render(str(n), True, line_color2)
        win.blit(num, (positions[f"x{n}"] + 80, positions[f"y{n}"] + 35))

    show_score()
    button1.draw(win, (255, 255, 255))
    button2.draw(win, (255, 255, 255))
    pygame.display.update()

grid()
count = 0   # Contador del algoritmo de búsqueda 

find_nums(board) 
running = True  

while running:
    translate_board() 
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1.isOver(pos):  # Clic en el boton "Resolver"
                button1.color = (255,0,0)
                button1.text = "Buscando"

                total_moves = 0
                count = 0
                translate_board()
                initial = copy.deepcopy(board)
                board_previous = copy.deepcopy(board)

                def is_solvable(board):
                    flat_board = [num for row in board for num in row if num != 0]
                    inversions = sum(1 for i in range(len(flat_board) - 1) for j in range(i + 1, len(flat_board)) if flat_board[i] > flat_board[j])
                    return inversions % 2 == 0

                def backtrack(n1):
                    current = n1
                    g_score = 0
                    solved = current == board_solved

                    while not solved or current != came_from["previous_node0"]:
                        if solved:
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
                            
                def distance():
                    man = 0
                    for i in range(1, 9):
                        x1, y1 = find(board, i)
                        x2, y2 = find(board_solved, i)
                        distance = abs(x2 - x1) + abs(y2 - y1)
                        man += distance
                    return man

                def RLrestrict():
                    global allow_r, allow_l
                    allow_r = all(board[i][2] != 0 for i in range(3))
                    allow_l = all(board[i][0] != 0 for i in range(3))

                def UDrestrict():
                    global allow_u, allow_d
                    allow_u = all(board[0][i] != 0 for i in range(3))
                    allow_d = all(board[2][i] != 0 for i in range(3))

                def find(board, num):
                    for i in range(len(board)):
                        for j in range(len(board[0])):
                            if board[i][j] == num:
                                return (i, j)  # row, col

                def right():
                    i, j = find(board, 0)
                    board[i][j], board[i][j + 1] = board[i][j + 1], board[i][j]
                    return board

                def up():
                    i, j = find(board, 0)
                    board[i][j], board[i - 1][j] = board[i - 1][j], board[i][j]
                    return board

                def left():
                    i, j = find(board, 0)
                    board[i][j], board[i][j - 1] = board[i][j - 1], board[i][j]
                    return board

                def down():
                    i, j = find(board, 0)
                    board[i][j], board[i + 1][j] = board[i + 1][j], board[i][j]
                    return board
                
                class Node:
                    def __init__(self, position, f_score):
                        self.position = position
                        self.f_score = f_score

                def in_closed(n1):
                    return n1 == closed_set.get("start", None) or n1 in closed_set.values()

                n1 = Node(board, distance())
                open_set = PriorityQueue()
                nodes = {}
                closed_set = {}
                came_from = {}
                closed_set["start"] = copy.deepcopy(board)

                if is_solvable(board):
                    while board != board_solved:
                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                        RLrestrict()
                        UDrestrict()
                        if allow_r:
                            n1.position = right()
                            if in_closed(n1.position):
                                left()
                            if not in_closed(n1.position):
                                nodes["node%s" % count] = n1.position
                                came_from["previous_node%s" % count] = copy.deepcopy(left())
                                n1.position = copy.deepcopy(right())
                                h_score = distance()
                                n1.f_score = h_score + backtrack(n1.position)
                                open_set.put((n1.f_score, h_score, count, n1.position))
                                board = copy.deepcopy(board_previous)
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
                        find_nums(board)  
                        redraw_window()

                        if board == board_solved:
                            print("RESUELTO")
                            break
                        closed_set["node%s" % count] = copy.deepcopy(next_item)
                        board_previous = copy.deepcopy(board)
                    else:
                        print("NO TIENE SOLUCIÓN")

                    print(str(len(closed_set)) + " nodos explorados")
                    print(str(len(nodes)) + " total de nodos")
                    total_moves = 0
                    for n in range(0, len(solved_moves)):  
                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)  
                        time.sleep(1)  
                        find_nums(solved_moves["move%s" % (len(solved_moves) - n - 1)])
                        redraw_window()
                        if n != len(solved_moves) - 1:
                            total_moves += 1
                    solved_moves = {}
                    button1.color = (0, 255, 0)
                    button1.text = "Resolver"
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
            else:
                button1.color = (0,255,0)
                button1.text = "Resolver"

            if button2.isOver(pos):  # Reinicia el tablero a la posición inicial
                button2.color = (255,0,0)
                board = copy.deepcopy(initial)
                find_nums(board)
                redraw_window()
                button2.color = (0,255,0)
                total_moves = 0      
                initial = copy.deepcopy(board)

    keys = pygame.key.get_pressed()
    redraw_window()
pygame.quit()
