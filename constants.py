############
# Tablero
############
SIZE = 100
GRID_LEN = 6 #celdas por lado
GRID_PADDING = 5 # separación de celdas
GRID_WITH_SCORE = GRID_LEN + 1

########################
# Puntuacion para ganar
########################
OBJECTIVE = 32

########################
# Fichero log de salida
########################
FICHERO_LOG = "logs/log_automatic_play.json"

############
# Movimientos
############
MOVEMENTS = ["Down","Left", "Up", "Right"]

############
# Numeros
############
# Numeros que aparecen tras hacer un movimiento
RANDOM_NUMBER_CHOICES = [2, 4]
# Probabilidad de cada número de aparecer
PROBAB_NUMBER_CHOICES = [0.7, 0.3]

############
# Tiempos
############
# Tiempo a esperar cuando se gana / pierde con la situación de la partida
TIME_WAIT_FINISH_GAME = 5 # segundos

# Tiempo que espera la máquina en automatic_play.py para el siguiente movimientos
TIME_CPU_NEXT_MOVEMENT = 0.2 #segundos


####################
# Scores colores
####################
# Score colores
BACKGROUND_SCORE = "#00B1E7"

#Font Score
FONT_SCORE = "#37013C"

############
# Colores
############

# Classic
#BACKGROUND_COLOR_GAME = "#92877d"
#BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"

# New
BACKGROUND_COLOR_GAME = "#310038"
BACKGROUND_COLOR_CELL_EMPTY = "#04E8F5"

# Color font winning and losing game:
COLOR_FONT_FINAL_MESSAGE = "#37013C"

#Color background
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
                         16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
                         128: "#edcf72", 256: "#edcc61", 512: "#edc850",
                         1024: "#edc53f", 2048: "#edc22e",

                         4096: "#eee4da", 8192: "#edc22e", 16384: "#f2b179",
                         32768: "#f59563", 65536: "#f67c5f", }

# Color font
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2",
                   256: "#f9f6f2", 512: "#f9f6f2", 1024: "#f9f6f2",
                   2048: "#f9f6f2",

                   4096: "#776e65", 8192: "#f9f6f2", 16384: "#776e65",
                   32768: "#776e65", 65536: "#f9f6f2", }

# Winning colores
LOSING_BG = "#f70158"
WINING_BG = "#00F883"
FINAL_FONT = "#300034"

#################
# Fuente texto
#################
FONT = ("Verdana", 20, "bold")
FONT_FINAL_MESSAGE = ("Verdana", 15, "bold")
