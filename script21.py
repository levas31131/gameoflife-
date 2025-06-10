import tkinter as tk
from LifeGame import LifeGame
from Rules import Rules

def main():
    """
    Funkcja startowa aplikacji. Tworzy okno i uruchamia grę.
    """
    root = tk.Tk()
    root.title("Game of Life")
    size, s, b = 30, "23", "3"

    rules = Rules(s, b)
    LifeGame(root, size, rules)
    root.mainloop()

if __name__ == "__main__":
    main()
