from sly import Lexer
import re

class CLexer(Lexer):
    tokens = {NUMBER, ID, EQ,  NE, LE, GE, AND, OR, PLUS,
              MINUS, MULTIPLY, DIVIDE, NOT, ASSIGN, TYPE, VOID, RETURN,
              PRINTF, STRING, SCANF, IF, ELSE , WHILE}

    # ignorar tabs
    ignore = ' \t'

    # caracteres literales
    literals = {'(', ')', ';', ',', '{', '}', '$','[',']', '&'}

    TYPE = r'int'
    VOID = r'void'
    PRINTF = r'printf'
    SCANF = r'scanf'
    IF = r'if'
    ELSE = r'else'
    WHILE = r'while'
    RETURN = r'return'
    NUMBER = r'[0-9]+'
    STRING = r'\"(\\.|[^\\"])*\"'  # Excluye caracteres especiales
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    PLUS = r'\+'
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
    


    @_(r'//.*')  # ignorar comentarios
    def ignorar_comentario(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1



    def tokenize(self, text):
        pattern = rf'({self.TYPE}|{self.VOID})\s+({self.ID})\s*\('

        match = re.search(pattern,text)
        pos = match.start()

        text = text[:pos] + '$' + text[pos:]




        original_tokens = super().tokenize(text)


        return original_tokens
        

