



def leer_fichero(nombre_fichero):
    try:
        with open(nombre_fichero, 'r', encoding='utf-8') as fichero:
            data = fichero.read()  # Lee todo el contenido del archivo
    except FileNotFoundError:
        print(f"El fichero {nombre_fichero} no existe.")
        data = None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        data = None
    return data



datos = leer_fichero("prueba.c")
print(datos)