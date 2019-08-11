2048-python
===========

# 0. Introduction

Se crea un nuevo repositorio a Git y se hace un clone del repositorio que copiamos:


```console
git clone https://github.com/yangshun/2048-python.git 2048
```


Se añade el nombre de la carpeta que queremos crear con ese proyecto.
En nuestro caso se crea en el drive D:/ en la carpeta Projectes

En GitHub se ha creado ya el repositorio vacío 2048. Vamos a SourceTree abrimos con "Add" el directorio 2048.

Ahora mismo, el repositorio sigue linkado a yangshun por lo que un push implica pedir permisos para modificar su código.
Como hemos creado ya nuestro propio repositorio vamos a "Settings", clicamos el origin y hacemos un "Edit", indicando la URL de Github con nuestro nuevo repositorio.

Una vez linkados, si hacemos cualquier cambio en esa carpeta, al hacer un commit y push, veremos que se actualiza en GitHub la carpeta y aparecen los ficheros del 2048.

## 0.1 Configurar ATOM para el interpreter de Python de Anaconda:

Abrir el Command Pallette (Control + Shift + P) en Atom y buscar "init script".

Nos deberá abrir el fichero "init.coffee" donde le ponemos lo siguiente:

```python
 process.env.PATH = ['C:\\Users\\David\\Anaconda3', process.env.PATH].join(':')
 ```

 Donde 'C:\\Users\\David\\Anaconda3' es el path donde se encuentra el ejecutable python.exe.

 De esta forma, al instalar autocomplete-python en Atom, cargará los paquetes que tengamos en ese interpreter.

 Luego ir a el paquete "autocomplete-python" y ir a Settings y vamos a la parte de "Python Executable Paths" y le metemos el path del python: "C:\Users\David\Anaconda3\python.exe". De esta forma ya deberíamos ver las sugerencias.

 Volvemos a descargar el paquete "Script" de Atom, y en el Menu Packages > Script vamos a "Configure Script" y a Command le metemos el path "C:\Users\David\Anaconda3\python.exe". Metemos click a "Save as profile" y le damos un nombre (version de python por ejemplo: py37). Luego, para ejecutar un bloque de codigo, solo hay que hacer click en "Run with profile" en   Packages > Script.

# 1. Test del código descargado

Procedemos a ejecutar el codigo descargado. Para ello, como lo hemos guardado en el drive D:/, hay que abrir el "Anaconda Prompt" en ese path... Para ello ejecutar:

```console
cd /d d:\Projectes\2048
```

# 2. Movimientos

Dada una matriz, primero hacemos los movimientos de mover todos los elementos no nulos al a derecha, izquierda, arriba o abajo.
Como el indexado de Python empieza por la izquierda y de arriba a abajo en las listas (matrices), observamos que con solo codificar el comando LEFT, las otras operaciones se pueden sacar haciendo rotaciones de matrices...

La operacion **LEFT** tiene 3 partes y 2 outputs (uno es la matriz ya desplazada y el segundo es un booleano de si ha habido algun movimiento o suma, da igual cual de los dos):
  - **Desplazamiento de numeros**: es una función que va mirando fila por fila, de izquierda a derecha si hay algun elemento no nulo. En tal caso, activa un contador, que lo que hace es va contando cuantos elementos no nulos hay en esa fila. A continuación, va situando estos elementos a su nueva posición (lo más a la izquierda posible), tal que al ser un contador, que se va actualizando a medidad que el bucle FOR recorre todas las columnas, en caso de encontrar 0 1 0 3 0 0 4 4 5 la posicion 0 es nula por lo que no activa el contador, la posicion 1 es un 1, por lo que pondrá ese 1 en la posicion del contador (de momento era el 0). Se suma un 1 al contador (contador = 1). La siguiente posicion es un 0, por lo que no activa nada. La siguiente (posicion 3) es un no nulo (3) por lo que colocará el 3 en la posicion 1 (ya que contador = 1) y se le suma 1 al contador (ahora contador = 2). Al llegar al 4, se coloca el 4 en la posición 2 y se suma 1 al contador. El 4 del final irá a la posición 3, etc... De este modo tendremos: 1 3 4 4 5 0 0 0 0. En caso de que en NINGUNA fila se haya movido ningún número con ese movimiento, se pondrá el booleano *done* a FALSE.
  - **Merging de numeros**: en el codigo de arriba solo se mueven numeros, por lo que queremos sumar los numeros que sean iguales. Eso hará que el primero de la pareja de numeros iguales (mirando siempre de izquierda a derecha esa fila) se actualize con calculando su doble (si hay un 4 4, se convertirá en 8 0) generando un 0 en el segundo numero. Obviamente, como el juego indica, al hacer un LEFT no puede haber espacios vacíos entre dos números mirandolos de izquierda a derecha, por lo que al hacer un merge de la secuencia de ejemplo anterior tendremos: 1 3 8 0 5 0 0 0 0. Eso claramente, requiere otro desplazamiento. Si hay un merging (se produce una suma de dos numeros iguales), se se pondrá el booleano *done* a TRUE.
  - **Desplazamiento de numeros**: se vuelve a aplicar el desplazamiento para, en caso de haber habido merging, mover todos los números a la izquierda y evitar que los 0 que salen del segundo sumando del merging estén entremedio de dos números. De este modo la fila de la matriz habría quedado: 1 3 8 5 0 0 0 0 0. Aquí no importa lo del *done* ya que si antes no se ha movido ni ha hecho merge nada, por mucho que aplicamos el desplazamiento, no hará nada, por lo que mantendrá el valor de *done* sea tanto TRUE como FALSE.

Si se tiene un poco de visión, se puede ver que todos los movimientos diferentes a LEFT, se puede codificar si se mira la matriz desde otro ángulo y se aplica un left en ese ángulo y a la matriz resultante se la vuelve a dar una vuelta contraria al ángulo que la habíamos mirado. Explicado así suena raro, y es difícil de entender si no se ve por lo que se propone mirar el caso de UP:

## 2.1 UP

Para hacer el desplazamiento y merging de todos los números hacia arriba, primero **rotamos la matriz de forma anti-horaria**

matriz inicial:

| 0 | 0 | 0 |
|---|---|---|
| 0 | 1 | 2 |
| 0 | 3 | 0 |

matriz rotada **anti-horario**:

| 0 | 2 | 0 |
|---|---|---|
| 0 | 1 | 3 |
| 0 | 0 | 0 |

aplicamos la operación **left**:

| 2 | 0 | 0 |
|---|---|---|
| 1 | 3 | 0 |
| 0 | 0 | 0 |

deshacemos la rotación rotando **horario**

| 0 | 1 | 2 |
|---|---|---|
| 0 | 3 | 0 |
| 0 | 0 | 0 |

que comparado con la matriz inicial vemos como ha provocado que todos los números suban arriba.

Se codifica las operaciones de rotación y left de la siguiente manera:

- **L**: left
- **H**: rotación horaria
- **AH**: rotación anti-horaria

De este modo, **la operación UP = AH - L - H**

## 2.2 DOWN

Es parecida a la UP, siendo **DOWN = H - L - AH**

## 2.3 RIGHT

Para hacer el RIGHT se pueden seguir diversas lógicas, una es primero rotar hacía la visión de un Down, y luego aplicar un Down y deshacer la rotación o rotar hacia un UP y aplicar el UP. Las dos combinaciones posibles son:

- **RIGHT option 1 = H - [H - L - AH] - AH**
- **RIGHT option 2 = AH - [AH - L - H] - H**

Notése que en los brackets hay las funciones de UP y DOWN implícitamente.
