from sly import Parser
from CLexer import CLexer

import time



'''S -> expr_list ';'

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

opUnario ->  opUn opMultDiv

opUn -> opUn '-'            // en C puede haber op unarios anidados
    | opUn '!'
    | '!'
    | '-'

opMultDiv -> opMultDiv '*' opSumaResta
	  | opMultDiv '/' opSumaResta
	  | opSumaResta

opSumaResta -> opSumaResta '+' term
	    | opSumaResta '-' term
	    | term

term -> ID
     | NUMBER

     '''





class CParser(Parser):
    # lexer
    tokens = CLexer.tokens

    precedence = (
    ('right', ASSIGN),
    ('left', OR),
    ('left', AND),
    ('left', EQ, NE, LE, GE),
    ('left', PLUS, MINUS),
    ('left', MULTIPLY, DIVIDE),
    ('right', NOT)
    )

      # S
    @_('expr_list ";"')
    def statement(self, p):

        #print("S")

        return p.expr_list

    # expr_list
    @_('expr_list ";" expr')
    def expr_list(self, p):
        return ('expr_list', p.expr_list, p.expr)

    @_('expr')
    def expr_list(self, p):
        return ('expr', p.expr)

    @_('";"')
    def statement(self, p):
        return 'empty_expr_list'

    # expr
    @_('lvalue ASSIGN opComp')
    def expr(self, p):
        return ('assign', p.lvalue, p.opComp)

    @_('opComp')
    def expr(self, p):
        return p.opComp

    # lvalue
    @_('lvalue ASSIGN ID')
    def lvalue(self, p):
        return ('assign_lvalue', p.lvalue, p.ID)

    @_('ID')
    def lvalue(self, p):
        return p.ID

    # opComp (comparaciones)
    @_('opComp EQ opLogOr')
    def opComp(self, p):
        return ('eq', p.opComp, p.opLogOr)

    @_('opComp NE opLogOr')
    def opComp(self, p):
        return ('ne', p.opComp, p.opLogOr)

    @_('opComp LE opLogOr')
    def opComp(self, p):
        return ('le', p.opComp, p.opLogOr)

    @_('opComp GE opLogOr')
    def opComp(self, p):
        return ('ge', p.opComp, p.opLogOr)

    @_('opLogOr')
    def opComp(self, p):
        return p.opLogOr

    # opLogOr
    @_('opLogOr OR opLogAnd')
    def opLogOr(self, p):
        return ('or', p.opLogOr, p.opLogAnd)

    @_('opLogAnd')
    def opLogOr(self, p):
        return p.opLogAnd

    # opLogAnd
    @_('opLogAnd AND opUnario')
    def opLogAnd(self, p):
        return ('and', p.opLogAnd, p.opUnario)

    

    # opUnario
    @_('opUnario')
    def opLogAnd(self, p):
        return p.opUnario

    @_('opUn opMultDiv')
    def opUnario(self, p):
        return p.opUn * p.opMultDiv

    @_('opUn MINUS')
    def opUn(self, p):
        return -1 * p.opUn

    @_('opUn NOT')
    def opUn(self, p):
        return not p.opUn

    @_('NOT')
    def opUn(self, p):
        return False

    @_('MINUS')
    def opUn(self, p):
        return -1


    

    #opMultDiv
    @_('opMultDiv')
    def opUnario(self, p):
        return p.opMultDiv

    # opMultDiv
    @_('opMultDiv MULTIPLY opSumaResta')
    def opMultDiv(self, p):
        return ('multiply', p.opMultDiv, p.opSumaResta)

    @_('opMultDiv DIVIDE opSumaResta')
    def opMultDiv(self, p):
        return ('divide', p.opMultDiv, p.opSumaResta)

    @_('opSumaResta')
    def opMultDiv(self, p):
        return p.opSumaResta

    # opSumaResta
    @_('opSumaResta PLUS term')
    def opSumaResta(self, p):

        # print("soy una suma ")
        return ('plus', p.opSumaResta, p.term)

    @_('opSumaResta MINUS term')
    def opSumaResta(self, p):
        return ('minus', p.opSumaResta, p.term)

    @_('term')
    def opSumaResta(self, p):
        return p.term

    # term rules (variables or numbers)
    @_('ID')
    def term(self, p):
        return ('id', p.ID)

    @_('NUMBER')
    def term(self, p):
        #print("soy un numero")
        return ('num', int(p.NUMBER))

if __name__ == '__main__':
    lexer = CLexer()
    parser = CParser()

    textos = {"a = b + c;", "a = 6 - 2;" , "a = !b != c;" , "a == c;" , "a = b*c/d = 56;", "; ; ;"}



    for texto in textos:
        print("\n\n\n\n",texto," :")
        tokens = lexer.tokenize(texto)
        result = parser.parse(tokens)
        print(result)
