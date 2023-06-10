from __future__ import print_function

import tkinter as tk
import tkinter.messagebox as messagebox

import sys
import random


class Grid:
    '''The data structure representation of the 2048 game.
    '''
    def __init__(self, n):
        self.size = n
        self.cells = self.generate_empty_grid()
        self.compressed = False
        self.merged = False
        self.moved = False
        self.current_score = 0

    def random_cell(self):
        cell = random.choice(self.retrieve_empty_cells())
        i = cell[0]
        j = cell[1]
        self.cells[i][j] = 2 if random.random() < 0.9 else 4

    def retrieve_empty_cells(self):
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] == 0:
                    empty_cells.append((i, j))
        return empty_cells

    def generate_empty_grid(self):
        return [[0] * self.size for i in range(self.size)]

    def transpose(self):
        self.cells = [list(t) for t in zip(*self.cells)]

    def reverse(self):
        for i in range(self.size):
            start = 0
            end = self.size - 1
            while start < end:
                self.cells[i][start], self.cells[i][end] = \
                    self.cells[i][end], self.cells[i][start]
                start += 1
                end -= 1

    def clear_flags(self):
        self.compressed = False
        self.merged = False
        self.moved = False

    def left_compress(self):
        self.compressed = False
        new_grid = self.generate_empty_grid()
        for i in range(self.size):
            count = 0
            for j in range(self.size):
                if self.cells[i][j] != 0:
                    new_grid[i][count] = self.cells[i][j]
                    if count != j:
                        self.compressed = True
                    count += 1
        self.cells = new_grid

    def left_merge(self):
        self.merged = False
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.cells[i][j] == self.cells[i][j + 1] and \
                   self.cells[i][j] != 0:
                    self.cells[i][j] *= 2
                    self.cells[i][j + 1] = 0
                    self.current_score += self.cells[i][j]
                    self.merged = True

    def found_2048(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] >= 2048:
                    return True
        return False

    def has_empty_cells(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] == 0:
                    return True
        return False

    def can_merge(self):
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.cells[i][j] == self.cells[i][j + 1]:
                    return True
        for j in range(self.size):
            for i in range(self.size - 1):
                if self.cells[i][j] == self.cells[i + 1][j]:
                    return True
        return False

    def set_cells(self, cells):
        self.cells = cells

    def print_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.cells[i][j], end='\t')
            print()

import sys
import tkinter as tk

class GamePanel:
    '''The GUI view class of the 2048 game showing via tkinter.'''
    CELL_PADDING = 10
    BACKGROUND_COLOR = '#92877d'
    EMPTY_CELL_COLOR = '#9e948a'
    CELL_BACKGROUND_COLOR_DICT = {
        '2': '#eee4da',
        '4': '#ede0c8',
        '8': '#f2b179',
        '16': '#f59563',
        '32': '#f67c5f',
        '64': '#f65e3b',
        '128': '#edcf72',
        '256': '#edcc61',
        '512': '#edc850',
        '1024': '#edc53f',
        '2048': '#edc22e',
        'beyond': '#3c3a32'
    }
    CELL_COLOR_DICT = {
        '2': '#776e65',
        '4': '#776e65',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#f9f6f2',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',
        'beyond': '#f9f6f2'
    }
    FONT = ('Verdana', 24, 'bold')
    UP_KEYS = ('w', 'W', 'Up')
    LEFT_KEYS = ('a', 'A', 'Left')
    DOWN_KEYS = ('s', 'S', 'Down')
    RIGHT_KEYS = ('d', 'D', 'Right')

    def __init__(self, grid):
        self.grid = grid
        self.root = tk.Tk()
        if sys.platform == 'win32':
            self.root.iconbitmap('2048.ico')
        self.root.title('2048')
        self.root.resizable(False, False)
        self.background = tk.Frame(self.root, bg=GamePanel.BACKGROUND_COLOR)
        self.cell_labels = []
        for i in range(self.grid.size):
            row_labels = []
            for j in range(self.grid.size):
                label = tk.Label(self.background, text='',
                                 bg=GamePanel.EMPTY_CELL_COLOR,
                                 justify=tk.CENTER, font=GamePanel.FONT,
                                 width=4, height=2)
                label.grid(row=i, column=j, padx=10, pady=10)
                row_labels.append(label)
            self.cell_labels.append(row_labels)
        self.background.pack(side=tk.TOP)

    def paint(self):
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                cell_value = self.grid.cells[i][j]
                if cell_value == 0:
                    self.cell_labels[i][j].configure(text='',
                                                     bg=GamePanel.EMPTY_CELL_COLOR)
                else:
                    cell_text = str(cell_value)
                    bg_color = GamePanel.CELL_BACKGROUND_COLOR_DICT.get(cell_text, GamePanel.CELL_BACKGROUND_COLOR_DICT['beyond'])
                    fg_color = GamePanel.CELL_COLOR_DICT.get(cell_text, GamePanel.CELL_COLOR_DICT['beyond'])
                    self.cell_labels[i][j].configure(text=cell_text,
                                                     bg=bg_color, fg=fg_color)


class Game:
    def __init__(self, size):
        self.size = size
        self.grid = Grid(size)
        self.root = tk.Tk()
        self.root.title('2048 Game')
        self.root.geometry('400x400')
        self.root.bind("<Key>", self.key_press)

        self.score_label = tk.Label(self.root, text="Score: 0")
        self.score_label.pack()

        self.canvas = tk.Canvas(self.root, bg='white', width=400, height=400)
        self.canvas.pack()

        self.init_game()

        self.root.mainloop()

    def init_game(self):
        self.grid.set_cells(self.grid.generate_empty_grid())
        self.grid.random_cell()
        self.grid.random_cell()
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        for i in range(self.size):
            for j in range(self.size):
                value = self.grid.cells[i][j]
                self.canvas.create_rectangle(
                    j * 100, i * 100, (j + 1) * 100, (i + 1) * 100, fill='gray')
                self.canvas.create_text(
                    (j * 100 + 50), (i * 100 + 50), text=str(value), font=("Arial", 24, "bold"))
        self.score_label.config(text="Score: " + str(self.grid.current_score))

    def key_press(self, event):
        key = event.keysym
        if key == 'Up' or key == 'Down' or key == 'Left' or key == 'Right':
            self.grid.clear_flags()
            self.handle_movement(key)
            self.update_canvas()

            if self.grid.found_2048():
                messagebox.showinfo("2048", "Congratulations! You win!")
                self.root.quit()
            elif not self.grid.has_empty_cells() and not self.grid.can_merge():
                messagebox.showinfo("2048", "Game Over!")
                self.root.quit()

    def handle_movement(self, key):
        if key == 'Up':
            self.grid.transpose()
            self.grid.reverse()
            self.grid.left_compress()
            self.grid.left_merge()
            self.grid.left_compress()
            self.grid.reverse()
            self.grid.transpose()
        elif key == 'Down':
            self.grid.transpose()
            self.grid.left_compress()
            self.grid.left_merge()
            self.grid.left_compress()
            self.grid.transpose()
        elif key == 'Left':
            self.grid.left_compress()
            self.grid.left_merge()
            self.grid.left_compress()
        elif key == 'Right':
            self.grid.reverse()
            self.grid.left_compress()
            self.grid.left_merge()
            self.grid.left_compress()
            self.grid.reverse()
        self.grid.random_cell()


if __name__ == '__main__':
    game = Game(4)
