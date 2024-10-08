from sly import Lexer

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
