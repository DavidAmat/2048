import random
import numpy as np
import constants as c

# Inicializa la matrix en blanco (4x4) lista de listas
def new_game(n):
    matrix = []

    for i in range(n):
        matrix.append([0] * n)
    return matrix

##################################################################
# Inicializa la matrix con un numero alli donde no haya 0
##################################################################


def add_two(mat):
    a = random.randint(0, len(mat)-1)
    b = random.randint(0, len(mat)-1)
    while(mat[a][b] != 0):
        # Si ya existe esa posicion(ya hay un 2), elige otra
        a = random.randint(0, len(mat)-1)
        b = random.randint(0, len(mat)-1)
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
#           Movimientos
############################################

#Algunos movimientos se pueden simplificar codificando un solo movimiento
# y los otros se puede aplicar el mismo movimeinto con la matrix revertida
# o traspuesta.

def displacement_numbers(mat):
    """
    Desplaza todos los elementos de la matriz a la izquierda
    """
    new = new_game(GRID_LEN) # crea una matrix de 0 de AxA (donde A es la GRID_LEN)
    done = False
    for i in range(GRID_LEN):
        # Inspecciona una fila
        count = 0
        for j in range(GRID_LEN):
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

# ////////
#   LEFT
# ////////
def left(game):
    print("left")
    # return matrix after shifting left
    game, done = cover_up(game)
    temp = merge(game)
    game = temp[0]
    done = done or temp[1]
    game = cover_up(game)[0]
    return (game, done)



# ////////
#   UP
# ////////
# El movimiento UP es como hacer una transpuesta, hacer un LEFT y volverla a trasponer
def up(game):
    print("up")
    # return matrix after shifting up
    game = transpose(game)
    game, done = cover_up(game)
    temp = merge(game)
    game = temp[0]
    done = done or temp[1]
    game = cover_up(game)[0]
    game = transpose(game)
    return (game, done)

def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

###########
# Task 2b #
###########

# [Marking Scheme]
# Points to note:
# 0 marks for completely incorrect solutions
# 1 mark for solutions that show general understanding
# 2 marks for correct solutions that work for all sizes of matrices


# def transpose(mat):
#     new = []
#     for i in range(len(mat[0])):
#         new.append([])
#         for j in range(len(mat)):
#             new[i].append(mat[j][i])
#     return new



##########
# Task 3 #
##########

# [Marking Scheme]
# Points to note:
# The way to do movement is compress -> merge -> compress again
# Basically if they can solve one side, and use transpose and reverse correctly they should
# be able to solve the entire thing just by flipping the matrix around
# No idea how to grade this one at the moment. I have it pegged to 8 (which gives you like,
# 2 per up/down/left/right?) But if you get one correct likely to get all correct so...
# Check the down one. Reverse/transpose if ordered wrongly will give you wrong result.


def cover_up(mat):
    new = new_game(c.GRID_LEN)
    done = False
    for i in range(c.GRID_LEN):
        count = 0
        for j in range(c.GRID_LEN):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return (new, done)


def merge(mat):
    done = False
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j+1] = 0
                done = True
    return (mat, done)





def down(game):
    print("down")
    game = reverse(transpose(game))
    game, done = cover_up(game)
    temp = merge(game)
    game = temp[0]
    done = done or temp[1]
    game = cover_up(game)[0]
    game = transpose(reverse(game))
    return (game, done)




def right(game):
    print("right")
    # return matrix after shifting right
    game = reverse(game)
    game, done = cover_up(game)
    temp = merge(game)
    game = temp[0]
    done = done or temp[1]
    game = cover_up(game)[0]
    game = reverse(game)
    return (game, done)
