import random
from tkinter import Frame, Label, CENTER
import time
# Importamos codigos .py
import movements as mov
import constants as c


class GameGrid(Frame):
    def __init__(self):
        ##################################
        # Crear frame de TKinter
        ##################################
        Frame.__init__(self)
        self.grid()
        self.master.title('2048 by David')

        ######################################################
        # Activar una acción al pulsar una tecla de direccion
        ######################################################
        for arrow in c.MOVEMENTS:
            self.master.bind("<{0}>".format(arrow), # si se teclea una arrow
                lambda event, key_pressed = arrow: self.key_arrow(key_pressed))
                # pasale a la funcion un argumento llamado key_pressed con el nombre de la arrow

        #############################################
        # # DESHACER MOVIMIENTO con la tecla "b"
        #############################################
        self.master.bind("<b>", self.key_back)

        ##################################
        # Linkar tecla arrow con funcion
        ##################################
        # El nombre de cada arrow llama a la funcion con su mismo nombre (getattrib)
        # de la clase getattr llama a la funcion con el nombre "down" por ejemplo
        self.commands = {}
        for arrow in c.MOVEMENTS:
            self.commands[arrow] = getattr(mov, arrow.lower())

        ##################################
        # Crear array de celdas
        ##################################
        self.grid_cells = []

        ##################################
        # Inicializacion del juego
        ##################################
        #ESTADO ACTIVO:
        self.game_status_active = 0 # activo
        self.init_grid()
        self.init_matrix() #matriz con 2 numeros 2
        self.update_grid_cells()

        #########################################
        # Resta a la espera de recibir teclas
        #########################################
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

    def init_matrix(self):
        # Llama al script mov y crea una matrix de zeros
        # [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.matrix = mov.new_game(c.GRID_LEN)

        # HISTORICO de MATRICES para ir hacia atras en caso de pulsar tecla "b"
        self.history_matrixs = list()

        # Añade dos 2 en unas posiciones random (nunca se solaparans)
        self.matrix = mov.add_two(self.matrix, times = 2)


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
        self.update_idletasks()

    def show_message(self, winning = True):
        self.grid_cells[1][1].configure(
            text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY,
            fg = c.COLOR_FONT_FINAL_MESSAGE)
        if winning:
            self.grid_cells[1][2].configure(
                text="win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                fg = c.COLOR_FONT_FINAL_MESSAGE)
        else:
            self.grid_cells[1][2].configure(
                text="lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                fg = c.COLOR_FONT_FINAL_MESSAGE)
        self.update_idletasks()


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
        self.matrix, done, _ = self.commands[key_pressed](self.matrix)
        if done: # Si ha cambiado algo
            # añade un nuevo numero (numero random: ver movements.py)
            self.matrix = mov.add_two(self.matrix, rand_num_choice = True)
            # Record last move
            self.history_matrixs.append(self.matrix)
            self.update_grid_cells()
            done = False # cambiamos el done por si afecta en la siguiente iteración

            #############
            # GAME STATUS
            #############
            current_game_state = mov.game_state(self.matrix)
            if  current_game_state== "win":
                self.show_message(winning = True)
                self.game_status_active = 1 # ganado
                self.after(c.TIME_WAIT_FINISH_GAME*1000, self.end_game())

            elif current_game_state == "lose":
                self.show_message(winning = False)
                self.game_status_active = 2 # perdido
                self.after(c.TIME_WAIT_FINISH_GAME*1000, self.end_game())

    def end_game(self):
        self.quit()


gamegrid = GameGrid()
if gamegrid.game_status_active== 1:
    print("SE HA GANADO")
elif gamegrid.game_status_active== 2:
    print("SE HA PERDIDO")

time.sleep(3)
