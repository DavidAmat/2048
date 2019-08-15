import random
import time
import numpy as np
import json
import sys

# Importamos codigos .py
import movements as mov
import constants as c


class BackendPlayer():
    def __init__(self):
        self.movimientos = 0;
        self.grid_cells = []
        self.game_score = 0;
        self.log = {'mat': [], 'mov': [''], 'scores': [0]}
        self.commands = {'up': mov.up, 'down': mov.down,
                        'left': mov.left, 'right': mov.right}
        self.game_status_active = 0 # activo

        # Iniciamos matriz
        self.init_matrix()

        # Empezamos a jugar
        self.start()

    def init_matrix(self):
        self.matrix = mov.new_game(c.GRID_LEN)
        self.matrix = mov.add_two(self.matrix, times = 2)
        self.log["mat"].append(np.array(self.matrix).tolist())

    def start(self):
        while True:
            if self.game_status_active == 0:
                self.start_playing()
            else:
                break

    def start_playing(self):
        if self.game_status_active == 0:
            choice_movement = ["up", "down", "left", "right"]
            hay_movimiento = False
            while not hay_movimiento:
                # Mientras no se mueva la matriz, buscaremos otro comando
                movimiento = np.random.choice(choice_movement)
                hay_movimiento = self.key_arrow(movimiento)

                if self.game_status_active>0:
                    return

            #Guardamos en el log el movimiento escogido
            self.log["mov"].append(movimiento)
            self.log["mat"].append(np.array(self.matrix).tolist())
            self.log["scores"].append(int(self.game_score))
            # Actualiza el numero de movimientos realizados
            self.movimientos += 1

    def key_arrow(self, key_pressed):
        hay_movimiento = False
        # Reemplaza la matrix por la matriz actualizada despues del movimiento
        self.matrix, done, self.game_score = self.commands[key_pressed](self.matrix, self.game_score)
        if done: # Si ha cambiado algo
            # añade un nuevo numero (numero random: ver movements.py)
            self.matrix = mov.add_two(self.matrix, rand_num_choice = True)

            #############
            # GAME STATUS
            #############
            current_game_state = mov.game_state(self.matrix)
            if  current_game_state== "win":
                self.game_status_active = 1 # ganado
                self.end_game(key_pressed)

            elif current_game_state == "lose":
                self.game_status_active = 2 # perdido
                self.end_game(key_pressed)
        return done

    def end_game(self, key_pressed):
        self.log["mov"].append(key_pressed)
        self.log["mat"].append(np.array(self.matrix).tolist())
        self.log["scores"].append(int(self.game_score))
        #####################
        # LOG
        #####################
        # Guardamos en el log el resultado de la partida
        self.log["final"] = int(self.game_status_active)
        self.log["score"] = int(self.game_score)
        #Guarda el fichero en JSON con el encoding UTF-8
        with open(c.FICHERO_LOG, 'w') as f:
            json.dump(self.log, f)
        #sys.exit()

BackendPlayer()
