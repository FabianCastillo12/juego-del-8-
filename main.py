"""
Puzzle 8 Solver - Main Entry Point

This is the main entry point for the Puzzle 8 Solver application.
Run this file to start the GUI application.
"""

import tkinter as tk
from puzzle_gui import PuzzleGUI


def main():
    """Inicializa y ejecuta la aplicación"""
    root = tk.Tk()
    PuzzleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
