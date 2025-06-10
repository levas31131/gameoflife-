import json
import tkinter as tk
from tkinter import filedialog
import numpy as np

class LifeGame:
    """
    Główna klasa implementująca grę w życie (Conway's Game of Life) z GUI w Tkinterze.

    :param window: Obiekt głównego okna aplikacji (tk.Tk).
    :param cells: Rozmiar planszy (liczba komórek w pionie i poziomie).
    :param rules: Obiekt klasy Rules zawierający zasady gry.
    """

    def __init__(self, window, cells, rules):
        self.window = window
        self.size = cells
        self.cell_px = 20
        self.active = False
        self.rules = rules

        self.grid = np.zeros((cells, cells), dtype=int)

        self.canvas = tk.Canvas(window, width=cells * self.cell_px,
                                height=cells * self.cell_px, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click_cell)

        self.panel = tk.Frame(window)
        self.panel.pack()

        tk.Button(self.panel, text="Start/Stop", command=self.start_stop).pack(side=tk.LEFT)
        tk.Button(self.panel, text="Next", command=self.next_step).pack(side=tk.LEFT)
        tk.Button(self.panel, text="Clear", command=self.clear).pack(side=tk.LEFT)
        tk.Button(self.panel, text="Save", command=self.save_state).pack(side=tk.LEFT)
        tk.Button(self.panel, text="Load", command=self.load_state).pack(side=tk.LEFT)

        tk.Label(self.panel, text="Survive:").pack(side=tk.LEFT)
        self.survive_entry = tk.Entry(self.panel, width=5)
        self.survive_entry.insert(0, "23")
        self.survive_entry.pack(side=tk.LEFT)

        tk.Label(self.panel, text="Born:").pack(side=tk.LEFT)
        self.born_entry = tk.Entry(self.panel, width=5)
        self.born_entry.insert(0, "3")
        self.born_entry.pack(side=tk.LEFT)

        tk.Button(self.panel, text="Update Rules", command=self.update_rules).pack(side=tk.LEFT)

        self.add_default()
        self.loop()

    def click_cell(self, event):
        """
        Zmienia stan komórki po kliknięciu (żywa ↔ martwa).

        :param event: Zdarzenie kliknięcia myszy.
        """
        x = event.x // self.cell_px
        y = event.y // self.cell_px
        self.grid[y, x] = 1 - self.grid[y, x]
        self.draw()

    def start_stop(self):
        """
        Uruchamia lub zatrzymuje automatyczną symulację gry.
        """
        self.active = not self.active

    def clear(self):
        """
        Czyści planszę — wszystkie komórki stają się martwe.
        """
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.draw()

    def save_state(self):
        """
        Zapisuje aktualny stan planszy i reguły gry do pliku JSON.
        """
        file_path = filedialog.asksaveasfilename(
            title="Save grid state",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                data = {
                    "grid": self.grid.tolist(),
                    "survive": self.survive_entry.get(),
                    "born": self.born_entry.get()
                }
                with open(file_path, "w") as f:
                    json.dump(data, f)
            except Exception as e:
                print(f"Failed to save: {e}")

    def load_state(self):
        """
        Wczytuje stan planszy i reguły gry z pliku JSON.
        """
        file_path = filedialog.askopenfilename(
            title="Load saved grid",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                grid_data = np.array(data["grid"])
                if grid_data.shape == self.grid.shape:
                    self.grid = grid_data
                    self.survive_entry.delete(0, tk.END)
                    self.survive_entry.insert(0, data.get("survive", "23"))

                    self.born_entry.delete(0, tk.END)
                    self.born_entry.insert(0, data.get("born", "3"))

                    self.update_rules()
                    self.draw()
                else:
                    print("Grid size mismatch.")
            except Exception as e:
                print(f"Failed to load: {e}")

    def update_rules(self):
        """
        Aktualizuje reguły gry na podstawie wpisów użytkownika.
        """
        survive = self.survive_entry.get()
        born = self.born_entry.get()
        if survive.isdigit() and born.isdigit():
            self.rules.set_rules(survive, born)

    def count_neighbors(self, x, y):
        """
        Zlicza żywych sąsiadów dla danej komórki.

        :param x: Współrzędna X komórki.
        :param y: Współrzędna Y komórki.
        :return: Liczba żywych sąsiadów.
        :rtype: int
        """
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % self.size, (y + dy) % self.size
                count += self.grid[ny, nx]
        return count

    def update_grid(self):
        """
        Przechodzi do następnego pokolenia na podstawie aktualnych zasad.
        """
        new_state = np.zeros_like(self.grid)
        for y in range(self.size):
            for x in range(self.size):
                n = self.count_neighbors(x, y)
                if self.grid[y, x] == 1:
                    new_state[y, x] = self.rules.is_alive_next(n)
                else:
                    new_state[y, x] = self.rules.should_be_born(n)
        self.grid = new_state

    def draw(self):
        """
        Rysuje wszystkie komórki na płótnie Tkintera.
        """
        self.canvas.delete("all")
        for y in range(self.size):
            for x in range(self.size):
                color = "black" if self.grid[y, x] else "white"
                self.canvas.create_rectangle(
                    x * self.cell_px, y * self.cell_px,
                    (x + 1) * self.cell_px, (y + 1) * self.cell_px,
                    fill=color, outline="gray"
                )

    def loop(self):
        """
        Główna pętla aplikacji — wykonuje krok symulacji co 200 ms, jeśli jest aktywna.
        """
        if self.active:
            self.update_grid()
        self.draw()
        self.window.after(200, self.loop)

    def next_step(self):
        """
        Wykonuje pojedynczy krok symulacji (bez auto-pętli).
        """
        self.update_grid()
        self.draw()

    def add_default(self):
        """
        Dodaje domyślny wzorzec komórek (glider) przy starcie aplikacji.
        """
        for x, y in [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]:
            self.grid[y, x] = 1
