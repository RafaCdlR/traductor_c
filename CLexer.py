from sly import Lexer



class CLexer(Lexer):
    tokens = {NUMBER ,ID, EQ,  NE, LE, GE, AND, OR , PLUS , MINUS , MULTIPLY , DIVIDE , NOT , ASSIGN, TYPE, RETURN }

    # ignorar tabs
    ignore = ' \t'

    # caracteres literales
    literals = {'(',')' ,';', ',', '{', '}'}


    TYPE = r'int|void'
    RETURN = r'return'
    NUMBER = r'[0-9]+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    PLUS  = r'\+'
    MINUS = r'-'
    MULTIPLY = r'\*'
    DIVIDE = r'/'
    EQ = r'=='
    NE = r'!='
    LE = r'<='
    GE = r'>='
    AND = r'&&'
    OR = r'\|\|'
    ASSIGN = r'='
    NOT = r'!'

    @_(r'//.*')#ignorar comentarios
    def ignorar_comentario(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

#prueba borrar luego
