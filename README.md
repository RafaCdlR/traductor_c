Para realizar una traducción ejecutar el comando:

	python3 src/main.py traducir.c traducido.s
	
donde traducir.c es el archivo a traducir y traducido.s es el archivo donde se guardará la traducción.


Usar `make probar` para ejecutar la prueba en `tests/cosas.c`.

No se aceptan varios ';' seguidos .

No se puede inicializar una variable en su declaración.
Para inicializarla, se hace en el cuerpo de una función.

Las declaraciones de las variables deben de ir al principio del código si son variables globales o al inicio de la función si son variables locales.
