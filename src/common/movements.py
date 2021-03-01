import numpy as np
import src.common.constants as c

class Movements():

    def __init__(self):
        pass

    @staticmethod
    def displacement_numbers(mat):
        """
        Desplaza todos los numeros a la izquierda de la matriz
        """

        new = np.zeros(mat.shape) # crea una matrix de 0 de AxA (donde A es la c.GRID_LEN)
        done = False
        for i in range(c.GRID_LEN):
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

    @staticmethod
    def merge_numbers(mat, game_score = 0):
        """
        Sum consecutive equal numbers (x) in a row
        ending with the second position being 0
        and the first position being the double of the number x
        Return also the number of merges done in all the matrix
        """
        num_merges = 0
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN -1): # la ultima columna j, no tiene una columna a su derecha (j+1)
                celda = mat[i][j]
                celda_derecha = mat[i][j +1]
                if celda == celda_derecha and celda != 0: # si son iguales, y esta igualdad son numeros > 0, se suman
                    merge_val = celda + celda_derecha
                    mat[i][j] = merge_val
                    game_score += merge_val  # suma los puntos
                    mat[i][j+1] = 0 # se deja la de la derecha vacía, esto hace que se necesite hacer otro displacement para llenar ese hueco
                    # esto tambien hace que al leer la siguiente columna, se lea un 0, y no el numero que estaba
                    num_merges += 1
        return (mat, num_merges, game_score)

    @staticmethod
    def perform_movement(game, game_score):
        """
        1 - mover al maximo a la izquierda todos los numeros
        2 - Sumamos los iguales dejando 0 en el segundo sumando
        3 - Por seguridad, por si hemos dejado alguno sin desplazar a la izquierda (huecos generados por el merge),
            se vuelve a aplicar sin importar el done o no (no importa si mueve a alguien o no ahora)
        """
        game_disp, done_disp = Movements.displacement_numbers(game)
        game_merged, num_merges, game_score = Movements.merge_numbers(game_disp, game_score)
        game_final = Movements.displacement_numbers(game_merged)[0]
        return (game_final, done_disp, num_merges, game_score)

    @staticmethod
    def ro(mat, cw = True, num = 1):  # cw: clockwise: True or False, #num: number of rotations
        """
        Rota 90º las matrices para que las operaciones UP, DOWN y RIGHT se puedan hacer con la de LEFT
        """
        param_clockise = (1 ,0) if cw else (0 ,1)  # clockwise or counter-clockwise (see help(np.rot90))

        # Cuantas rotaciones hacemos
        rot_mat = mat
        for _ in range(num):
            rot_mat = np.rot90(np.array(rot_mat), axes = param_clockise)

        return rot_mat

    @staticmethod
    def left(game, game_score = 0):
        return Movements.perform_movement(game, game_score)

    @staticmethod
    def down(game, game_score = 0):
        """
        C - L - UC
        """
        rotate_game = Movements.ro(game)  # rotate clockwise
        left_game, done, num_merges, game_score = Movements.left(rotate_game, game_score)  # apply left
        game_final = Movements.ro(left_game, cw = False)  # undo the rotation
        return game_final, done, num_merges, game_score

    @staticmethod
    def up(game, game_score = 0):
        """
        UC - L - C
        """
        rotate_game = Movements.ro(game, cw = False)  # rotate anti-clockwise
        left_game, done, num_merges, game_score = Movements.left(rotate_game, game_score)  # apply left
        game_final = Movements.ro(left_game)  # undo the rotation
        return game_final, done, num_merges, game_score

    @staticmethod
    def right(game, game_score = 0):
        """
        C - C - L - UC - UC
        """
        rotate_game = Movements.ro(game ,cw=True, num =2)  # double rotation
        left_game, done, num_merges, game_score = Movements.left(rotate_game, game_score)  # apply left
        game_final = Movements.ro(left_game, cw = False, num = 2)  # undo the rotation
        return game_final, done, num_merges, game_score