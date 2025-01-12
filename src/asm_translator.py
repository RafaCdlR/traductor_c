# Diccionario utilitario para traducir operadores a instrucciones en
# ensamblador
operdict = {
    '+': 'addl',
    '-': 'subl',
    '*': 'mull',
    '/': 'divl'
}

jumpcodes = {
    '>': 'jg',
    '>=': 'jge',
    '<': 'jl',
    '<=': 'jle',
    '==': 'je',
    '!=': 'jne'
}

# name es el nombre del fichero fuente
# crea el inicio del programa


def inicio_programa(name):
    return f".file {name}"


# id es el id de la variable global
# value es el valor inicial, por defecto none (sin inicialización)
# Devuelve el ensamblador correspondiente a la reserva de variables globales
def translate_global(id, value=None):
    stri = f".globl {id}\n\t"
    if not value:
        stri += f".zero\t{4}"
    else:
        stri += f".long\t{value}"

    return stri


# name es el nombre (string)
# param_number es el número de parámetros que recibe la función (int)
# code es el código YA TRADUCIDO A ENSAMBLADOR (string)
# ret_type es el tipo de return de la función (string)
#
# Produce el código de una función alrededor del código ya generado
# recibido por el argumento "code".
# No genera el código del return
def translate_funcion_def(name, param_number, code, ret_type):
    fname = f"{ret_type}_{name}"

    stri = f".globl {fname}\n"
    stri += f"{fname}:\n"
    # Prólogo de la función
    stri += "\tpushl %ebp\n\tmovl %esp, %ebp\n"

    stri += f"\tsubl ${4*param_number}, %esp\n"

    for line in code.splitlines():
        stri += f"\t{line}\n"

    # epílogo de la función
    stri += "\tmovl %ebp, %esp\n\tpopl %ebp"

    return stri


# oper = '+', '-', '*', '/'
# oper es la operación a realizar
# si off1 es int, se tratará como el offset de la variable 1, si no se tratará
# como el puntero global
# si off2 es int, se tratará como el offset de la variable 2, si no se tratará
# como el puntero global
def translate_oper(off1, off2, oper: str):

    stri = f'{operdict[oper]} %eax, %ebx'
    if type(off1 == int):
        off1 = f'-{off1}(%ebp)'
    if type(off2 == int):
        off2 = f'-{off2}(%ebp)'

    return f'movl {off1}, %ebx\nmovl {off2}, %eax\n' + stri


# Para casos donde hace falta acceder a pila u obtener alguna dirección, es
# más sencillo acceder a la operación directamente y traducirlo
def raw_oper(oper: str):
    return f'{operdict[oper]} %eax, %ebx'


# params: array de strings, almacena strings de la forma %ebp+offset para
# variables locales o con el nombre de la variable global
def call_function(name: str, params: list):
    assembled = ""
    for i in reversed(params):
        assembled += f"movl {i}, %eax\n"
    assembled += f"call {name}\n"
    assembled += f"addl ${4*len(params)}, %esp"

    return assembled
