import random
from tkinter import Frame, Label, CENTER
import time
# Importamos codigos .py
import logic
import constants as c


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title('2048 by David')

        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left,
                         c.KEY_RIGHT_ALT: logic.right}
        self.grid_cells = []

        # COMANDOS de INICIALIZACION y JUEGO
        self.init_grid()
        #print("Init grid \n")
        #time.sleep(4)
        #print("Init matrix \n")
        self.init_matrix() #matriz con 2 numeros 2

        #time.sleep(4)
        #print("Update cells \n")
        self.update_grid_cells()
        self.mainloop()


    def init_grid(self):
        # Creamos un cuadrado con un fondo de color game
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid() #lo pintamos

        #Creamos la grid
        for i in range(c.GRID_LEN): #fila
            grid_row = []
            for j in range(c.GRID_LEN): #columna
                # Declaramos un objeto cell de la clase Frame con las dimensiones
                # Cada celda tien longitud SIZE / numero de celdas
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                           pady=c.GRID_PADDING)
                # Para ese objeto cell, declaramos sus propiedades
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()

                #Generamos para cada fila, una lista de objetos label
                grid_row.append(t)

            # Lista de listas de cada celda, donde el primer elemento (que es una lista)
            # corresponde a la primera fila (cada subelemento de la lista será una columna)
            self.grid_cells.append(grid_row)

    def gen(self):
        """
        Genera un numero aleatorio en [0,1,2,3] (numero de celdas en una fila / columna)
        """
        return random.randint(0, c.GRID_LEN - 1)

    def init_matrix(self):
        # Llama al script logic y crea una matrix de zeros
        # [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = list()

        # Añade un 2 en una posicion random
        self.matrix = logic.add_two(self.matrix)

        # Añade un 2 en una posicion random diferente a la primera
        self.matrix = logic.add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                # Mira si en esa celda ya hay un numero o hay un 0
                if new_number == 0:
                    #Pintala como empty
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    # SI hay un numero, ve al diccionario de colores
                    # para ver el font color (fg) y el color de fondo
                    # de la celda (bg) ya que depende del numero
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number])
        #self.update_idletasks()


gamegrid = GameGrid()
