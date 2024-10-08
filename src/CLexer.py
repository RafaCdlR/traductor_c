from sly import Lexer



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



class CLexer(Lexer):
    tokens = { ID, INT, NUMBER }
    ignore = ' \t'
    literals = { '=', '==', '>=', '<=', '!=', '&&', '||', '!', '+', '-', '*', '/', '//', '/*', '*/' }

    INT = 'int'
    NUMBER = r'[0-9]+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
