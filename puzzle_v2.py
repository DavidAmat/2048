import random
from tkinter import Frame, Label, CENTER
import time
# Importamos codigos .py
import movements as logic
import constants as c


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title('2048 by David')
        #Cuando pulsemos una tecla de las arrows, le pasaremos a la funcion self.KEY_DOWN
        # como argumento la tecla que se haya presionado
        # MOVIMIENTOS
        arrows = ["Down","Left", "Up", "Right"]
        for arrow in arrows:
            self.master.bind("<{0}>".format(arrow), # si se teclea una arrow
                lambda event, key_pressed = arrow: self.key_arrow(key_pressed))
                # pasale a la funcion un argumento llamado key_pressed con el nombre de la arrow

        # DESHACER MOVIMIENTO con la tecla "b"
        self.master.bind("<b>", self.key_back)

        # LLAMA a las funciones de MOVEMENTS que hacen el LEFT; UP; RIGHT; DOWN
        self.commands = {"Down": logic.down,
                         "Left": logic.left,
                         "Up": logic.up,
                         "Right": logic.right}
        self.grid_cells = []

        # COMANDOS de INICIALIZACION y JUEGO
        self.init_grid()
        self.init_matrix() #matriz con 2 numeros 2
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

        # HISTORICO de MATRICES para ir hacia atras en caso de pulsar tecla "b"
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
                    try:
                        color_back = c.BACKGROUND_COLOR_DICT[new_number]
                        color_font = c.CELL_COLOR_DICT[new_number]
                    except:
                        color_back = "#FF5733"
                        color_font = "#FFDBD6"
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=color_back,
                        fg=color_font)
        #self.update_idletasks()

    # CONFIGURACION BOTON ATRAS
    def key_back(self, event):
        """
        Si se pulsa la tecla b, vamos al histórico de movimientos y sacamos la matriz última que tengamos
        Sirve como deshacer movimiento
        """
        if len(self.history_matrixs) > 1:
            # Recuperamos la penultima matriz (la ultima es la actual por lo que no se considera un deshacer)
            self.matrix = self.history_matrixs.pop(-2)
            print("Going back to step:", len(self.history_matrixs))
            self.update_grid_cells()
        else:
            print("No previous movements detected, please do a movement with arrows")

    def key_arrow(self, key_pressed):
        # Reemplaza la matrix por la matriz actualizada despues del movimiento
        self.matrix, done  = self.commands[key_pressed](self.matrix)
        if done:
            # Si ha cambiado algo, añade un nuevo numero
            self.matrix = logic.add_two(self.matrix, rand_num_choice = True)
            # Record last move
            self.history_matrixs.append(self.matrix)
            self.update_grid_cells()
            done = False # cambiamos el done por si afecta en la siguiente iteración


gamegrid = GameGrid()
