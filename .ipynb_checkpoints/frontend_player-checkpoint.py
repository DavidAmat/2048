import random
import time
import numpy as np
import json
import sys
from tkinter import Frame, Label, CENTER, Canvas
# Importamos codigos .py
import movements as mov
import constants as c
import backend_player as BK

def read_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


class FrontEndPlay(Frame):
    def __init__(self):
        ##################################
        # Crear frame de TKinter
        ##################################
        Frame.__init__(self)
        self.grid()
        self.master.title('2048 by David')
        self.movimientos = 0;
        self.grid_cells = []
        self.log = read_json(c.FICHERO_LOG)


        ##################################
        # Inicializacion del juego
        ##################################
        self.game_status_active = 0
        self.init_grid()

        # Cargamos la matriz inicial
        self.matrix = self.log["mat"][0]

        # Loop de todos los pasos realizados
        for iter in range(1, len(self.log["mat"])):
            time.sleep(c.TIME_CPU_NEXT_MOVEMENT)
            self.update_grid_cells(iter)
            self.update()
            if iter == (len(self.log["mat"])-1):
                self.show_message(iter)



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
                t_score = Label(master=score_cell, text="Score: 0",
                          bg=c.BACKGROUND_SCORE,
                          fg=c.FONT_SCORE,
                          justify=CENTER, font=c.FONT,
                          width=c.SIZE // 6,
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

    def update_grid_cells(self, iter):
        for i in range(c.GRID_WITH_SCORE):
            if i == 0:
                # Update SCORE
                self.grid_cells[i][0].configure(
                text="Score: {0}".format(self.log["scores"][iter]),
                fg=c.FONT_SCORE,
                bg=c.BACKGROUND_SCORE
                )
                continue
            for j in range(c.GRID_LEN):
                new_number = self.log["mat"][iter][i-1][j]
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


    def show_message(self, iter):
        status = self.log["final"]
        if status == 1:
            winning = True
            color = c.WINING_BG
            message = "You win!"
        elif status == 2:
            winning = False
            color = c.LOSING_BG
            message = "You lost!"

        # Update SCORE
        self.grid_cells[0][0].configure(
        text="{0} Score: {1}".format(message, self.log["scores"][iter]), #TODO
        fg=c.FINAL_FONT, font = c.FONT_FINAL_MESSAGE,
        bg=color, width = c.SIZE // 5)
        self.update()
        time.sleep(c.TIME_WAIT_FINISH_GAME)
        self.quit()

# Hacemos jugar a la maquina
start_timer = time.time()
BK.BackendPlayer()
end_timer = time.time()

print("Tiempo juego:", round(end_timer - start_timer,4))
# Visualizamos la partida
#FrontEndPlay()
