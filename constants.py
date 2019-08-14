SIZE = 100
GRID_LEN = 6
GRID_PADDING = 5
OBJECTIVE = 128

# MOVIMIENTOS
MOVEMENTS = ["Down","Left", "Up", "Right"]
MAX_NUM_MOV = 10

# Numeros que aparecen tras hacer un movimiento
RANDOM_NUMBER_CHOICES = [2, 4]
# Probabilidad de cada número de aparecer
PROBAB_NUMBER_CHOICES = [0.7, 0.3]

############
# Tiempos
############
# Tiempo a esperar cuando se gana / pierde con la situación de la partida
TIME_WAIT_FINISH_GAME = 2 # segundos

# Tiempo que espera la máquina en automatic_play.py para el siguiente movimientos
TIME_CPU_NEXT_MOVEMENT = 0.1 #segundos

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"

# Color font winning and losing game:
COLOR_FONT_FINAL_MESSAGE = "#6B5B95"

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

FONT = ("Verdana", 30, "bold")
