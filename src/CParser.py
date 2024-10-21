from sly import Parser
from CLexer import CLexer


'''

S -> def_list ';' expr_list ';'

def_list -> def_list ';' def
	 | def
	 | epsilon

def -> tipo defd

defd -> defd, ID
    | ID

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
    debugfile = 'parser.out'
    variables = dict()
    precedence = (
        ('right', ASSIGN),
        ('left', OR),
        ('left', AND),
        ('left', EQ, NE, LE, GE),
        ('left', PLUS, MINUS),
        ('left', MULTIPLY, DIVIDE),
        ('right', NOT),
    )

    # FUNCIONES AUXILIARES
    def anadir_variable(self, tipo, nombre):

        if nombre not in self.variables:

            if tipo == "int":
                self.variables[nombre] = 0
            else:
                raise Exception("tipo no valido")

        else:

            raise Exception("variable ", nombre, " ya declarada anteriormente")

    # S
    @_('defi_list expr_list')
    def statement(self, p):
        return (p.defi_list, p.expr_list)

    @_('defi_list')
    def statement(self, p):
        return (p.defi_list, [])

    @_('expr_list')
    def statement(self, p):
        return ([], p.expr_list)

    # def_list (lista de definiciones, permite múltiples declaraciones)

    # def_list (lista de definiciones, permite múltiples declaraciones)
    @_('defi_list defi ";"')
    def defi_list(self, p):
        return p.defi_list + [p.defi]

    @_('defi ";"')
    def defi_list(self, p):
        return [p.defi]

    # def (declaración individual)
    @_('TYPE id_list')
    def defi(self, p):
        for id in p.id_list:
            self.anadir_variable(p.TYPE, id)
        return [(p.TYPE, id) for id in p.id_list]




    # Lista de identificadores separados por comas
    @_('ID "," id_list')
    def id_list(self, p):
        return [p.ID] + p.id_list

    @_('ID')
    def id_list(self, p):
        return [p.ID]


    # Caso vacío
    @_('')
    def defi_list(self, p):
        return []
    # expr_list

    @_('expr_list ";" expr')
    def expr_list(self, p):
        return ('expr_list', p.expr_list, p.expr)

    @_('expr ";"')
    def expr_list(self, p):
        return ('expr', p.expr)

    # expr
    @_('lvalue ASSIGN opComp')
    def expr(self, p):
        return ('assign', p.lvalue, p.opComp)

    @_('opComp')
    def expr(self, p):
        return p.opComp

    # @_('')
    # def expr(self, p):
        # pass

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

    # opMultDiv

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
        # print("soy un numero")
        return ('num', int(p.NUMBER))


if __name__ == '__main__':
    lexer = CLexer()
    parser = CParser()

    textos = {"a = b + c;", "a = 6 - 2;", "a = !b != c;", "a == c;",
              "a = b*c/d = 56;", "; ; ;", "int a;", "int f; int b; int c;", "int a", "int j, k, l;"}

    for texto in textos:
        try:
            print("\n\n\n\n", texto, " :")
            tokens = lexer.tokenize(texto)
            result = parser.parse(tokens)
            print(result)
        except Exception as err:
            print(f"Error de compilación: {err}")

    print("tabla de variables :")

    for clave, valor in parser.variables.items():

        print(type(valor), " ", clave, " = ", valor)
