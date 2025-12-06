"""
Puzzle 8 Solver - GUI Interface

This module contains the graphical user interface for the puzzle solver application.
Uses tkinter for the UI components.
"""

import tkinter as tk
from tkinter import messagebox
import time
from puzzle_solver import a_star, is_solvable


class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Solver del Puzzle 8 - Algoritmo A*")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e2e")

        # Estados
        self.board_initial = (
            (6, 5, 1),
            (2, 8, 7),
            (3, 4, 0),
        )

        self.board_solved = (
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 0),
        )

        self.current_state = self.board_initial
        self.solution_path = []
        self.current_step = 0
        self.stats = {}

        # Colores modernos
        self.colors = {
            "bg": "#1e1e2e",
            "tile": "#89b4fa",
            "tile_hover": "#74c7ec",
            "empty": "#313244",
            "text": "#cdd6f4",
            "accent": "#f38ba8",
            "success": "#a6e3a1",
            "button": "#89b4fa",
            "button_hover": "#74c7ec",
        }

        self.create_widgets()
        self.draw_board(self.current_state)

    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""

        # Título
        title_frame = tk.Frame(self.root, bg=self.colors["bg"])
        title_frame.pack(pady=20)

        title = tk.Label(
            title_frame,
            text="🎮 SOLVER DEL PUZZLE 8",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["accent"],
        )
        title.pack()

        subtitle = tk.Label(
            title_frame,
            text="Algoritmo A* con Heurística de Manhattan",
            font=("Segoe UI", 12),
            bg=self.colors["bg"],
            fg=self.colors["text"],
        )
        subtitle.pack()

        # Frame principal con dos columnas
        main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Columna izquierda - Tablero
        left_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        left_frame.pack(side=tk.LEFT, padx=20)

        # Canvas para el tablero
        self.canvas = tk.Canvas(
            left_frame,
            width=400,
            height=400,
            bg=self.colors["bg"],
            highlightthickness=0,
        )
        self.canvas.pack(pady=10)

        # Indicador de paso
        self.step_label = tk.Label(
            left_frame,
            text="Paso: 0 / 0",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["success"],
        )
        self.step_label.pack(pady=10)

        # Botones de navegación
        nav_frame = tk.Frame(left_frame, bg=self.colors["bg"])
        nav_frame.pack(pady=10)

        self.btn_prev = tk.Button(
            nav_frame,
            text="◀ Anterior",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["button"],
            fg="white",
            activebackground=self.colors["button_hover"],
            command=self.prev_step,
            state=tk.DISABLED,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
        )
        self.btn_prev.pack(side=tk.LEFT, padx=5)

        self.btn_next = tk.Button(
            nav_frame,
            text="Siguiente ▶",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["button"],
            fg="white",
            activebackground=self.colors["button_hover"],
            command=self.next_step,
            state=tk.DISABLED,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
        )
        self.btn_next.pack(side=tk.LEFT, padx=5)

        # Columna derecha - Controles y estadísticas
        right_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20)

        # Botones principales
        control_frame = tk.Frame(right_frame, bg=self.colors["bg"])
        control_frame.pack(pady=20)

        self.btn_solve = tk.Button(
            control_frame,
            text="🚀 Resolver Puzzle",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["success"],
            fg="#1e1e2e",
            activebackground="#94e2d5",
            command=self.solve_puzzle,
            relief=tk.FLAT,
            padx=30,
            pady=15,
            cursor="hand2",
        )
        self.btn_solve.pack(pady=10)

        self.btn_edit = tk.Button(
            control_frame,
            text="✏️ Editar Estados",
            font=("Segoe UI", 12, "bold"),
            bg="#f9e2af",
            fg="#1e1e2e",
            activebackground="#f5c2e7",
            command=self.edit_states,
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
        )
        self.btn_edit.pack(pady=10)

        self.btn_reset = tk.Button(
            control_frame,
            text="🔄 Reiniciar",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["accent"],
            fg="white",
            activebackground="#eba0ac",
            command=self.reset,
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
        )
        self.btn_reset.pack(pady=10)

        # Panel de estadísticas
        stats_frame = tk.LabelFrame(
            right_frame,
            text="📊 Estadísticas",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            relief=tk.FLAT,
            borderwidth=2,
        )
        stats_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.stats_labels = {}
        stats_items = [
            ("Movimientos óptimos:", "moves"),
            ("Nodos explorados:", "explored"),
            ("Nodos generados:", "generated"),
            ("Eficiencia:", "efficiency"),
            ("Tiempo de ejecución:", "time"),
        ]

        for text, key in stats_items:
            frame = tk.Frame(stats_frame, bg=self.colors["bg"])
            frame.pack(pady=8, padx=20, fill=tk.X)

            tk.Label(
                frame,
                text=text,
                font=("Segoe UI", 11),
                bg=self.colors["bg"],
                fg=self.colors["text"],
            ).pack(side=tk.LEFT)

            value_label = tk.Label(
                frame,
                text="-",
                font=("Segoe UI", 11, "bold"),
                bg=self.colors["bg"],
                fg=self.colors["accent"],
            )
            value_label.pack(side=tk.RIGHT)
            self.stats_labels[key] = value_label

        # Estado objetivo
        goal_frame = tk.LabelFrame(
            right_frame,
            text="🎯 Estado Objetivo",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            relief=tk.FLAT,
            borderwidth=2,
        )
        goal_frame.pack(pady=10, fill=tk.X)

        self.goal_text = tk.Label(
            goal_frame,
            text=self.format_state_display(self.board_solved),
            font=("Consolas", 14, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["success"],
            justify=tk.CENTER,
        )
        self.goal_text.pack(pady=10)

    def draw_board(self, state):
        """Dibuja el tablero en el canvas"""
        self.canvas.delete("all")

        tile_size = 120
        gap = 10
        offset_x = 20
        offset_y = 20

        for i in range(3):
            for j in range(3):
                num = state[i][j]
                x1 = offset_x + j * (tile_size + gap)
                y1 = offset_y + i * (tile_size + gap)
                x2 = x1 + tile_size
                y2 = y1 + tile_size

                # Color de la casilla
                if num == 0:
                    color = self.colors["empty"]
                    text_color = self.colors["text"]
                    text = "·"
                else:
                    color = self.colors["tile"]
                    text_color = "white"
                    text = str(num)

                # Dibujar casilla con sombra
                self.canvas.create_rectangle(
                    x1 + 3, y1 + 3, x2 + 3, y2 + 3, fill="#11111b", outline=""
                )

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="", tags=f"tile_{i}_{j}"
                )

                # Número
                self.canvas.create_text(
                    (x1 + x2) // 2,
                    (y1 + y2) // 2,
                    text=text,
                    font=("Segoe UI", 36, "bold"),
                    fill=text_color,
                )

    def solve_puzzle(self):
        """Ejecuta el algoritmo A* y muestra la solución"""
        self.btn_solve.config(state=tk.DISABLED)

        start_time = time.time()
        result, nodes_explored, nodes_generated = a_star(
            self.board_initial, self.board_solved
        )
        end_time = time.time()
        execution_time = end_time - start_time

        if result:
            self.solution_path = result
            self.current_step = 0

            # Actualizar estadísticas
            self.stats = {
                "moves": len(result) - 1,
                "explored": nodes_explored,
                "generated": nodes_generated,
                "efficiency": f"{(nodes_explored / nodes_generated * 100):.1f}%",
                "time": f"{execution_time:.4f}s",
            }

            self.stats_labels["moves"].config(text=str(self.stats["moves"]))
            self.stats_labels["explored"].config(text=str(self.stats["explored"]))
            self.stats_labels["generated"].config(text=str(self.stats["generated"]))
            self.stats_labels["efficiency"].config(text=self.stats["efficiency"])
            self.stats_labels["time"].config(text=self.stats["time"])

            # Habilitar botones de navegación
            self.btn_next.config(state=tk.NORMAL)
            self.update_step_display()

            messagebox.showinfo(
                "✅ Solución Encontrada",
                f"Puzzle resuelto en {len(result) - 1} movimientos óptimos!\n\n"
                f"Usa los botones para ver la solución paso a paso.",
            )
        else:
            messagebox.showerror(
                "❌ Sin Solución",
                "Este puzzle no tiene solución desde el estado inicial dado.",
            )
            self.btn_solve.config(state=tk.NORMAL)

    def next_step(self):
        """Muestra el siguiente paso de la solución"""
        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.current_state = self.solution_path[self.current_step]
            self.draw_board(self.current_state)
            self.update_step_display()

            # Actualizar botones
            self.btn_prev.config(state=tk.NORMAL)
            if self.current_step >= len(self.solution_path) - 1:
                self.btn_next.config(state=tk.DISABLED)

    def prev_step(self):
        """Muestra el paso anterior de la solución"""
        if self.current_step > 0:
            self.current_step -= 1
            self.current_state = self.solution_path[self.current_step]
            self.draw_board(self.current_state)
            self.update_step_display()

            # Actualizar botones
            self.btn_next.config(state=tk.NORMAL)
            if self.current_step <= 0:
                self.btn_prev.config(state=tk.DISABLED)

    def update_step_display(self):
        """Actualiza el indicador de paso actual"""
        total = len(self.solution_path) - 1 if self.solution_path else 0
        self.step_label.config(text=f"Paso: {self.current_step} / {total}")

    def reset(self):
        """Reinicia la aplicación al estado inicial"""
        self.current_state = self.board_initial
        self.solution_path = []
        self.current_step = 0

        self.draw_board(self.current_state)
        self.update_step_display()

        # Resetear estadísticas
        for label in self.stats_labels.values():
            label.config(text="-")

        # Resetear botones
        self.btn_solve.config(state=tk.NORMAL)
        self.btn_prev.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.DISABLED)

    def format_state_display(self, state):
        """Formatea un estado como string para mostrar"""
        lines = []
        for row in state:
            line = " ".join([str(num) if num != 0 else "·" for num in row])
            lines.append(line)
        return "\n".join(lines)

    def validate_state(self, values):
        """Valida que el estado sea válido (números 0-8 sin repetir)"""
        try:
            nums = [int(v) for v in values]
            if len(nums) != 9:
                return False, "Debe haber exactamente 9 números"
            if sorted(nums) != list(range(9)):
                return False, "Debe contener los números 0-8 sin repetir"
            return True, ""
        except ValueError:
            return False, "Todos los valores deben ser números"

    def edit_states(self):
        """Abre un diálogo para editar los estados inicial y objetivo"""
        # Crear ventana modal
        dialog = tk.Toplevel(self.root)
        dialog.title("✏️ Editar Estados")
        dialog.geometry("600x500")
        dialog.configure(bg=self.colors["bg"])
        dialog.transient(self.root)
        dialog.grab_set()

        # Título
        title = tk.Label(
            dialog,
            text="Editar Estados del Puzzle",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["accent"],
        )
        title.pack(pady=20)

        # Frame principal
        main_frame = tk.Frame(dialog, bg=self.colors["bg"])
        main_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Estado Inicial
        initial_frame = tk.LabelFrame(
            main_frame,
            text="📍 Estado Inicial",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            relief=tk.FLAT,
            borderwidth=2,
        )
        initial_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        initial_entries = []
        for i in range(3):
            row_frame = tk.Frame(initial_frame, bg=self.colors["bg"])
            row_frame.pack(pady=5)
            for j in range(3):
                entry = tk.Entry(
                    row_frame,
                    width=3,
                    font=("Segoe UI", 16, "bold"),
                    bg="#313244",
                    fg="#cdd6f4",
                    justify=tk.CENTER,
                    relief=tk.FLAT,
                    insertbackground="#cdd6f4",
                )
                entry.pack(side=tk.LEFT, padx=3)
                entry.insert(
                    0,
                    str(self.board_initial[i][j])
                    if self.board_initial[i][j] != 0
                    else "0",
                )
                initial_entries.append(entry)

        # Estado Objetivo
        goal_frame = tk.LabelFrame(
            main_frame,
            text="🎯 Estado Objetivo",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            relief=tk.FLAT,
            borderwidth=2,
        )
        goal_frame.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)

        goal_entries = []
        for i in range(3):
            row_frame = tk.Frame(goal_frame, bg=self.colors["bg"])
            row_frame.pack(pady=5)
            for j in range(3):
                entry = tk.Entry(
                    row_frame,
                    width=3,
                    font=("Segoe UI", 16, "bold"),
                    bg="#313244",
                    fg="#cdd6f4",
                    justify=tk.CENTER,
                    relief=tk.FLAT,
                    insertbackground="#cdd6f4",
                )
                entry.pack(side=tk.LEFT, padx=3)
                entry.insert(
                    0,
                    str(self.board_solved[i][j])
                    if self.board_solved[i][j] != 0
                    else "0",
                )
                goal_entries.append(entry)

        # Instrucciones
        instructions = tk.Label(
            dialog,
            text="💡 Ingresa los números 0-8 (usar 0 para el espacio vacío)",
            font=("Segoe UI", 10),
            bg=self.colors["bg"],
            fg=self.colors["text"],
        )
        instructions.pack(pady=10)

        # Botones
        btn_frame = tk.Frame(dialog, bg=self.colors["bg"])
        btn_frame.pack(pady=20)

        def apply_changes():
            # Obtener valores
            initial_values = [entry.get().strip() for entry in initial_entries]
            goal_values = [entry.get().strip() for entry in goal_entries]

            # Validar estado inicial
            valid_initial, msg_initial = self.validate_state(initial_values)
            if not valid_initial:
                messagebox.showerror("Error - Estado Inicial", msg_initial)
                return

            # Validar estado objetivo
            valid_goal, msg_goal = self.validate_state(goal_values)
            if not valid_goal:
                messagebox.showerror("Error - Estado Objetivo", msg_goal)
                return

            # Convertir a tuplas
            initial_nums = [int(v) for v in initial_values]
            goal_nums = [int(v) for v in goal_values]

            new_initial = (
                tuple(initial_nums[0:3]),
                tuple(initial_nums[3:6]),
                tuple(initial_nums[6:9]),
            )

            new_goal = (
                tuple(goal_nums[0:3]),
                tuple(goal_nums[3:6]),
                tuple(goal_nums[6:9]),
            )

            # Verificar si el estado inicial es resoluble
            if not is_solvable(new_initial):
                result = messagebox.askyesno(
                    "⚠️ Estado No Resoluble",
                    "El estado inicial ingresado NO tiene solución matemática.\n\n"
                    "¿Deseas aplicarlo de todos modos?",
                )
                if not result:
                    return

            # Aplicar cambios
            self.board_initial = new_initial
            self.board_solved = new_goal
            self.current_state = self.board_initial

            # Actualizar visualización
            self.draw_board(self.current_state)
            self.goal_text.config(text=self.format_state_display(self.board_solved))

            # Resetear solución
            self.solution_path = []
            self.current_step = 0
            self.update_step_display()

            # Resetear estadísticas
            for label in self.stats_labels.values():
                label.config(text="-")

            # Resetear botones
            self.btn_solve.config(state=tk.NORMAL)
            self.btn_prev.config(state=tk.DISABLED)
            self.btn_next.config(state=tk.DISABLED)

            dialog.destroy()
            messagebox.showinfo(
                "✅ Estados Actualizados",
                "Los estados inicial y objetivo han sido actualizados correctamente.",
            )

        btn_apply = tk.Button(
            btn_frame,
            text="✅ Aplicar Cambios",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["success"],
            fg="#1e1e2e",
            activebackground="#94e2d5",
            command=apply_changes,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
        )
        btn_apply.pack(side=tk.LEFT, padx=5)

        btn_cancel = tk.Button(
            btn_frame,
            text="❌ Cancelar",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["accent"],
            fg="white",
            activebackground="#eba0ac",
            command=dialog.destroy,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)
