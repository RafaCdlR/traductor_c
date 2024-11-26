class variable:
    name: str
    type: str
    init: int = None


# name es el nombre del fichero fuente
# crea el inicio del programa
def inicio_programa(name):
    return f".file {name}"


# id es el id de la variable global
# value es el valor inicial, por defecto none (sin inicialización)
# Devuelve el ensamblador correspondiente a la reserva de variables globales
def translate_global(id, value=None):
    str = f".globl {id}\n\t"
    if not value:
        str += f".zero\t{4}"
    else:
        str += f".long\t{value}"


# name es el nombre (string)
# param_number es el número de parámetros que recibe la función (int)
# code es el código YA TRADUCIDO A ENSAMBLADOR (string)
# ret_type es el tipo de return de la función (string)
#
# Produce el código de una función alrededor del código ya generado
# recibido por el argumento "code".
# No genera el código del return
def translate_funcion(name, param_number, code, ret_type):
    fname = f"{ret_type}_{name}"

    str = f".globl {fname}\n"
    str += f"{fname}:\n"
    # Prólogo de la función
    str += "\tpushl %ebp\n\tmovl %esp, %ebp\n"

    str += f"\tsubl ${4*param_number}, %esp\n"

    for line in code.splitlines():
        str += f"\t{line}\n"

    # epílogo de la función
    str += "\tmovl %ebp, %esp\n\tpopl %ebp"

    return str
