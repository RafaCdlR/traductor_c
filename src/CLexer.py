from sly import Lexer



'''

S -> def_list ';' expr_list ';'

def_list -> def_list ';' def
	 | def
	 | epsilon

def -> tipo ID

expr_list -> expr_list ';' expr
           | expr
           | epsilon

expr -> lvalue '=' opComp
      | opComp

lvalue -> lvalue '=' ID
       | ID

opComp -> opComp '==' opLogOr
       | opComp '<=' opLogOr
       | opComp '>=' opLogOr
       | opComp '!=' opLogOr
       | opLogOr

opLogOr -> opLogOr '||' opLogAnd       // en C or tiene menos prioridad que and
	| opLogAnd

opLogAnd -> opLogAnd '&&' opUnario     // and menos prioridad que un op unario
	 | opUnario

opUnario -> '!' opUnario               // en C puede haber op unarios anidados
	 | '-' opUnario                // en C puede haber op unarios anidados
	 | opMultDiv

opMultDiv -> opMultDiv '*' opSumaResta
	  | opMultDiv '/' opSumaResta
	  | opSumaResta

opSumaResta -> opSumaResta '+' term
	    | opSumaResta '-' term
	    | term

term -> ID
     | NUMBER

     '''

class CLexer(Lexer):
    tokens = {NUMBER ,ID, EQ,  NE, LE, GE, AND, OR , PLUS , MINUS , MULTIPLY , DIVIDE , NOT , ASSIGN, TYPE }

    # ignorar tabs
    ignore = ' \t'

    # caracteres literales
    literals = {'(',')' ,';',','}


    TYPE = r'int'
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
