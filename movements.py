import random
import numpy as np
import constants as c

def new_game(n):
    """
    Inicializa la matrix en blanco (4x4) lista de listas
    """
    matrix = []

    for i in range(n):
        matrix.append([0] * n)
    return matrix

def add_two(mat, times = 1):
    """
    Busca aleatoriamente donde hay un 0 y le pone un 2 si esa celda
    está nula. Eso lo repetimos "times" veces
    """
    for _ in range(times):
        a, b = [random.randint(0, len(mat)-1) for _ in range(2)]
        while(mat[a][b] != 0):
            # Si ya existe esa posicion(ya hay un 2), elige otra
            a, b = [random.randint(0, len(mat)-1) for _ in range(2)]
        mat[a][b] = 2 #siempre inicializamos el juego con 2 numeros 2
    return mat

###########
# Task 1c #
###########

# [Marking Scheme]
# Points to note:
# Matrix elements must be equal but not identical
# 0 marks for completely wrong solutions
# 1 mark for getting only one condition correct
# 2 marks for getting two of the three conditions
# 3 marks for correct checking


def game_state(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return 'win'
    for i in range(len(mat)-1):
        # intentionally reduced to check the row on the right and below
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(len(mat[0])-1):
            if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                return 'not over'
    for i in range(len(mat)):  # check for any zero entries
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'
    for k in range(len(mat)-1):  # to check the left/right entries on the last row
        if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1):  # check up/down entries on last column
        if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'

############################################
#           Operaciones con matrices
############################################
# 3 herramientas: desplazar, merge y rotar

def displacement_numbers(mat):
    """
    Desplaza todos los numeros a la izquierda de la matriz
    """
    new = new_game(c.GRID_LEN) # crea una matrix de 0 de AxA (donde A es la c.GRID_LEN)
    done = False
    for i in range(c.GRID_LEN):
        # Inspecciona una fila
        count = 0
        for j in range(c.GRID_LEN):
            # Si en esa fila hay un elemento no nulo
            if mat[i][j] != 0:
                # Pone ese elemento en la posicion count (columna), donde esta vendra determinada por si
                # en esa fila, previamente, hemos encotrado algun otro elemento NO nulo
                new[i][count] = mat[i][j]

                # Solo con que modifiquemos la posicion de una de los numeros, ya contara como un movimiento: done = True
                if j != count:
                    done = True

                # Suma al count una posicion ya que ya se ha movido a la izquerda de todo (columna 0) ese elemento
                count += 1
    return (new, done)

def merge_numbers(mat):
    """
    Suma los números de cada fila que sean iguales y consecutivos, dejando el segundo sumando a 0
    """
    done = False
    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN-1): # la ultima columna j, no tiene una columna a su derecha (j+1)
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0: # si son iguales, y esta igualdad son numeros > 0, se suman
                mat[i][j] *= 2
                mat[i][j+1] = 0 # se deja la de la derecha vacía, esto hace que se necesite hacer otro displacement para llenar ese hueco
                # esto tambien hace que al leer la siguiente columna, se lea un 0, y no el numero que estaba
                done = True
    return (mat, done)

def ro(mat, cw = True, num = 1): #cw: clockwise: True or False, #num: number of rotations
    """
    Rota 90º las matrices para que las operaciones UP, DOWN y RIGHT se puedan hacer con la de LEFT
    """
    param_clockise = (1,0) if cw else (0,1) #clockwise or counter-clockwise (see help(np.rot90))

    # Cuantas rotaciones hacemos
    rot_mat = mat
    for _ in range(num):
        rot_mat = np.rot90(np.array(rot_mat), axes = param_clockise)

    return rot_mat.tolist()

############################################
#           MOVIMIENTO LEFT
############################################

def left(game):
    """
    1 - mover al maximo a la izquierda todos los numeros
    2 - Sumamos los iguales dejando 0 en el segundo sumando
    3 - Por seguridad, por si hemos dejado alguno sin desplazar a la izquierda (huecos generados por el merge),
        se vuelve a aplicar sin importar el done o no (no importa si mueve a alguien o no ahora)
    """
    game_disp, done_disp = displacement_numbers(game)
    game_merged, done_merge = merge_numbers(game_disp) #la salida es una tupla (mat, done)
    game_final = displacement_numbers(game_merged)[0]
    return (game_final, done_disp or done_merge)

def down(game):
    """
    C - L - UC
    """
    rotate_game = ro(game) #rotate clockwise
    left_game, done = left(rotate_game) #apply left
    game_final = ro(left_game, cw = False) #undo the rotation
    return game_final, done

def up(game):
    """
    UC - L - C
    """
    rotate_game = ro(game, cw = False) #rotate anti-clockwise
    left_game, done = left(rotate_game) #apply left
    game_final = ro(left_game) #undo the rotation
    return game_final, done

def right(game):
    """
    C - C - L - UC - UC
    """
    rotate_game = ro(game,cw=True, num =2) #double rotation
    left_game, done = left(rotate_game) #apply left
    game_final = ro(left_game, cw = False, num = 2) #undo the rotation
    return game_final, done
