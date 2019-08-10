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
