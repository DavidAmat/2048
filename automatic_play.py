import random
from tkinter import Frame, Label, CENTER, Canvas
import time
import numpy as np
# Importamos codigos .py
import movements as mov
import constants as c
import sys
import json
import threading
from tkinter.messagebox import showinfo

class AutomaticPlay(Frame):
    def __init__(self):
        ##################################
        # Crear frame de TKinter
        ##################################
        Frame.__init__(self)
        self.grid()
        self.master.title('2048 by David, AutomaticPlay')
        self.movimientos = 0;
        ##################################
        # Crear array de celdas
        ##################################
        self.grid_cells = []

        ##################################
        # Score
        ##################################
        self.game_score = 0;
        # para cada suma (i.e 8+8 se sumará 16 al game_score)

        ##################################
        # Log de la partida
        ##################################
        self.log = {}
        self.log["mat"] = [] # histórico de matrices
        self.log["mov"] = [''] #histórico de movimientos
        # como guardamos la primera matriz, el primer mov es nulo
        ##################################
        # Linkar tecla arrow con funcion
        ##################################
        self.commands = {'up': mov.up, 'down': mov.down,
                        'left': mov.left, 'right': mov.right}


        ##################################
        # Inicializacion del juego
        ##################################
        #ESTADO ACTIVO:
        self.game_status_active = 0 # activo
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        ###################################################
        # Ejecuta la orden de empezar a generar movimientos
        ###################################################
        self.start()




    ##################################
    # Dar órdenes
    ##################################
    def start(self):
        self.update()
        if self.game_status_active == 0:
            print("NUM MOV", self.movimientos)
            self.start_playing()

    def start_playing(self):
        time.sleep(c.TIME_CPU_NEXT_MOVEMENT)
        if self.game_status_active == 0:
            choice_movement = ["up", "down", "left", "right"]
            movimiento = np.random.choice(choice_movement)
            hay_movimiento = self.key_arrow(movimiento)

            #Guardamos en el log el movimiento escogido
            self.log["mov"].append(movimiento)
            self.log["mat"].append(np.array(self.matrix).tolist())

            # Actualiza el numero de movimientos realizados
            self.update_grid_cells()
            self.movimientos += 1

            #Si se siguie jugando, vuelve a llamar el metodo start
            if self.game_status_active == 0:
                # Imprime el movimiento realizado
                print("movimiento: ", movimiento)

                # Vuelve a correr el update y generar el thread de juego
                self.start()

    def init_grid(self):
        # Creamos un cuadrado con un fondo de color game
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid() #lo pintamos

        # creamos una fila antes para el score
        score_cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                     width= c.SIZE ,
                     height=c.SIZE / c.GRID_WITH_SCORE)
        score_cell.grid(
            row = 0,
            column = 0,
            columnspan = c.GRID_LEN ,
            padx=c.GRID_PADDING,
            pady=c.GRID_PADDING )

        #Creamos la grid
        for i in range(0, c.GRID_WITH_SCORE): #fila
            grid_row = []
            if i == 0:
                # SCORE ROW: creamos una fila con una celda para el score
                t_score = Label(master=score_cell, text="Score: {0}".format(self.game_score),
                          bg=c.BACKGROUND_SCORE,
                          fg=c.FONT_SCORE,
                          justify=CENTER, font=c.FONT,
                          width=c.SIZE // (6),
                          height= 2)

                t_score.grid()
                grid_row.append(t_score)
                self.grid_cells.append(grid_row)
                continue
            for j in range(1, c.GRID_WITH_SCORE): #columna
                # Declaramos un objeto cell de la clase Frame con las dimensiones
                # Cada celda tien longitud SIZE / numero de celdas
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE // (c.GRID_WITH_SCORE),
                             height=c.SIZE // (c.GRID_WITH_SCORE))
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

        #self.master.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        #self.master.columnconfigure((0,1,2,3,4,5,6), weight=1)

    def init_matrix(self):
        # Llama al script mov y crea una matrix de zeros
        self.matrix = mov.new_game(c.GRID_LEN)

        # HISTORICO de MATRICES para ir hacia atras en caso de pulsar tecla "b"
        self.history_matrixs = list()

        # Añade dos 2 en unas posiciones random (nunca se solaparans)
        self.matrix = mov.add_two(self.matrix, times = 2)

        # Guardamos esa matriz inicial
        self.log["mat"].append(np.array(self.matrix).tolist())

    def update_grid_cells(self):
        for i in range(c.GRID_WITH_SCORE):
            if i == 0:
                # Update SCORE
                self.grid_cells[i][0].configure(
                text="Score: {0}".format(self.game_score),
                fg=c.FONT_SCORE,
                bg=c.BACKGROUND_SCORE
                )
                continue
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i-1][j]
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


    def key_arrow(self, key_pressed):
        # Reemplaza la matrix por la matriz actualizada despues del movimiento
        self.matrix, done, self.game_score = self.commands[key_pressed](self.matrix, self.game_score)

        if done: # Si ha cambiado algo
            # añade un nuevo numero (numero random: ver movements.py)
            self.matrix = mov.add_two(self.matrix, rand_num_choice = True)
            # Record last move
            self.history_matrixs.append(self.matrix)
            self.update_grid_cells()

            #############
            # GAME STATUS
            #############
            current_game_state = mov.game_state(self.matrix)
            if  current_game_state== "win":
                self.game_status_active = 1 # ganado
                self.show_message()
                self.after(c.TIME_WAIT_FINISH_GAME*1000, self.end_game())

            elif current_game_state == "lose":
                self.game_status_active = 2 # perdido
                self.show_message()
                self.after(c.TIME_WAIT_FINISH_GAME*1000, self.end_game())
        return done

    def show_message(self):
        if self.game_status_active == 1:
            winning = True
            color = c.WINING_BG
            message = "You win!"
        else:
            winning = False
            color = c.LOSING_BG
            message = "You lost!"

        # Update SCORE
        self.grid_cells[0][0].configure(
        text="{0} Score: {1}".format(message, self.game_score), #TODO
        fg=c.FINAL_FONT, font = c.FONT_FINAL_MESSAGE, bg=color, width = c.SIZE // (5))

        self.update_idletasks()

    def end_game(self):
        if self.game_status_active == 1:
            print("GAME WON !")
            print("SCORE", self.game_score)
        else:
            print("GAME LOST!")
            print("SCORE", self.game_score)

        #####################
        # LOG
        #####################
        # Guardamos en el log el resultado de la partida
        self.log["final"] = int(self.game_status_active)
        self.log["score"] = int(self.game_score)
        #Guarda el fichero en JSON con el encoding UTF-8
        with open(c.FICHERO_LOG, 'w') as f:
            json.dump(self.log, f)

        # SALIMOS DEL JUEGO
        self.quit()

gamegrid = AutomaticPlay()
