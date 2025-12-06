from queue import PriorityQueue
import time

# Estado inicial del tablero
board_initial = (
    (6, 5, 1),
    (2, 8, 7),
    (3, 4, 0),
)

# Estado objetivo del tablero
board_solved = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0),
)


def tuple_to_board(state):
    """Convierte una tupla a lista para uso interno si es necesario"""
    return [list(row) for row in state]


def board_to_tuple(board):
    """Convierte un tablero (lista) a tupla inmutable"""
    return tuple(tuple(row) for row in board)


def is_solvable(board):
    """Verifica si el tablero es resoluble contando inversiones"""
    flat_board = [num for row in board for num in row if num != 0]
    inversions = sum(
        1
        for i in range(len(flat_board) - 1)
        for j in range(i + 1, len(flat_board))
        if flat_board[i] > flat_board[j]
    )
    return inversions % 2 == 0


def find_zero(state):
    """Encuentra la posición del espacio vacío (0)"""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None


def get_neighbors(state):
    """Genera todos los estados vecinos posibles (arriba, abajo, izquierda, derecha)"""
    neighbors = []
    board = tuple_to_board(state)
    i, j = find_zero(state)

    # Arriba
    if i > 0:
        new_board = [row[:] for row in board]
        new_board[i][j], new_board[i - 1][j] = new_board[i - 1][j], new_board[i][j]
        neighbors.append(board_to_tuple(new_board))

    # Abajo
    if i < 2:
        new_board = [row[:] for row in board]
        new_board[i][j], new_board[i + 1][j] = new_board[i + 1][j], new_board[i][j]
        neighbors.append(board_to_tuple(new_board))

    # Izquierda
    if j > 0:
        new_board = [row[:] for row in board]
        new_board[i][j], new_board[i][j - 1] = new_board[i][j - 1], new_board[i][j]
        neighbors.append(board_to_tuple(new_board))

    # Derecha
    if j < 2:
        new_board = [row[:] for row in board]
        new_board[i][j], new_board[i][j + 1] = new_board[i][j + 1], new_board[i][j]
        neighbors.append(board_to_tuple(new_board))

    return neighbors


def manhattan_distance(state, goal):
    """Calcula la distancia de Manhattan entre el estado actual y el objetivo"""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                num = state[i][j]
                # Encontrar posición objetivo del número
                for goal_i in range(3):
                    for goal_j in range(3):
                        if goal[goal_i][goal_j] == num:
                            distance += abs(i - goal_i) + abs(j - goal_j)
                            break
    return distance


def reconstruct_path(came_from, current):
    """Reconstruye el camino desde el inicio hasta el objetivo"""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def a_star(start, goal):
    """
    Implementación optimizada del algoritmo A*

    Returns:
        tuple: (path, nodes_explored, nodes_generated) o (None, nodes_explored, nodes_generated)
    """
    if not is_solvable(start):
        return None, 0, 0

    # Contador para desempatar en la PriorityQueue
    counter = 0

    # Cola de prioridad: (f_score, counter, state)
    open_set = PriorityQueue()
    open_set.put((0, counter, start))
    counter += 1

    # Diccionario para reconstruir el camino
    came_from = {}

    # Costo desde el inicio hasta cada nodo
    g_score = {start: 0}

    # Conjunto de estados ya explorados (cerrado)
    closed_set = set()

    # Nodos generados
    nodes_generated = 1
    nodes_explored = 0

    while not open_set.empty():
        # Obtener el nodo con menor f_score
        current_f, _, current = open_set.get()

        # Si ya fue explorado, continuar
        if current in closed_set:
            continue

        nodes_explored += 1

        # Si llegamos al objetivo, reconstruir camino
        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, nodes_explored, nodes_generated

        # Marcar como explorado
        closed_set.add(current)

        # Explorar vecinos
        for neighbor in get_neighbors(current):
            if neighbor in closed_set:
                continue

            # g_score es el costo desde el inicio hasta este vecino
            tentative_g_score = g_score[current] + 1

            # Si encontramos un mejor camino a este vecino
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                h_score = manhattan_distance(neighbor, goal)
                f_score = tentative_g_score + h_score

                open_set.put((f_score, counter, neighbor))
                counter += 1
                nodes_generated += 1

    # No se encontró solución
    return None, nodes_explored, nodes_generated


# Colores ANSI
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    RED = "\033[91m"
    GRAY = "\033[90m"


def print_board(state, show_step=False, step_num=0):
    """Imprime el tablero de forma elegante con formato de caja"""
    print(f"{Colors.CYAN}┌───────────┐{Colors.RESET}")
    for i, row in enumerate(state):
        formatted_row = " ".join(
            [
                f"{Colors.YELLOW}{num}{Colors.RESET}"
                if num != 0
                else f"{Colors.GRAY}·{Colors.RESET}"
                for num in row
            ]
        )
        print(
            f"{Colors.CYAN}│{Colors.RESET} {formatted_row} {Colors.CYAN}│{Colors.RESET}"
        )
    print(f"{Colors.CYAN}└───────────┘{Colors.RESET}")


def print_separator():
    """Imprime un separador visual"""
    print(f"{Colors.GRAY}{'─' * 50}{Colors.RESET}")


def print_header(text):
    """Imprime un encabezado destacado"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'═' * 50}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'═' * 50}{Colors.RESET}\n")


# Ejecutar el algoritmo
print_header("🎮 SOLVER DEL PUZZLE 8 - ALGORITMO A*")

print(f"{Colors.BOLD}Estado Inicial:{Colors.RESET}")
print_board(board_initial)

print(f"\n{Colors.BOLD}Estado Objetivo:{Colors.RESET}")
print_board(board_solved)

print(f"\n{Colors.YELLOW}⏳ Buscando solución...{Colors.RESET}\n")

start_time = time.time()
result, nodes_explored, nodes_generated = a_star(board_initial, board_solved)
end_time = time.time()
execution_time = end_time - start_time

if result:
    print_header(f"✅ PUZZLE RESUELTO EN {len(result) - 1} MOVIMIENTOS")

    # Mostrar TODOS los pasos completos
    for i, state in enumerate(result):
        print(f"{Colors.MAGENTA}▶ Paso {i}:{Colors.RESET}")
        print_board(state)
        print()

    # Estadísticas
    print_separator()
    print(f"{Colors.BOLD}{Colors.GREEN}📊 ESTADÍSTICAS:{Colors.RESET}")
    print(
        f"  {Colors.CYAN}•{Colors.RESET} Movimientos óptimos: {Colors.YELLOW}{len(result) - 1}{Colors.RESET}"
    )
    print(
        f"  {Colors.CYAN}•{Colors.RESET} Nodos explorados: {Colors.YELLOW}{nodes_explored}{Colors.RESET}"
    )
    print(
        f"  {Colors.CYAN}•{Colors.RESET} Nodos generados: {Colors.YELLOW}{nodes_generated}{Colors.RESET}"
    )
    print(
        f"  {Colors.CYAN}•{Colors.RESET} Eficiencia: {Colors.YELLOW}{(nodes_explored / nodes_generated * 100):.1f}%{Colors.RESET}"
    )
    print(
        f"  {Colors.CYAN}•{Colors.RESET} Tiempo de ejecución: {Colors.YELLOW}{execution_time:.4f}s{Colors.RESET}"
    )
    print_separator()
    print(f"{Colors.GREEN}✨ ¡Solución encontrada con éxito!{Colors.RESET}\n")
else:
    print_header("❌ PUZZLE NO RESOLUBLE")
    print(f"{Colors.RED}Este estado inicial no tiene solución.{Colors.RESET}\n")
    print(
        f"  {Colors.CYAN}•{Colors.RESET} Nodos explorados: {Colors.YELLOW}{nodes_explored}{Colors.RESET}"
    )
    print(
        f"  {Colors.CYAN}•{Colors.RESET} Nodos generados: {Colors.YELLOW}{nodes_generated}{Colors.RESET}\n"
    )
