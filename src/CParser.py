from sly import Parser
from CLexer import CLexer


class CParser(Parser):
    # lexer
    tokens = CLexer.tokens
    debugfile = 'parser.out'
    simbolos = dict()
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
    def anadir_simbolo(self, tipo, nombre , contenido = 0):

        if nombre not in self.simbolos:

            if tipo == "int":
                self.simbolos[nombre] = contenido
            elif tipo == "funcion":
                self.simbolos[nombre] = contenido
            else:
                raise Exception("tipo no valido")

        else:

            raise Exception("variable ", nombre, " ya declarada anteriormente")

    @_('globales "$" funciones')
    def S(self, p):
        for g in p.globales:
            print(g)
            self.anadir_simbolo(g[0],g[1])
        

        for f in p.funciones:
            self.anadir_simbolo("funcion",f[2],f)

        
        return (p.globales,p.funciones)

    @_('defi_list')
    def globales(self, p):
        return p.defi_list

    @_('')
    def globales(self, p):
        return None


    @_('funciones funcion')
    def funciones(self, p):
        return p.funciones + [p.funcion]

    @_('TYPE ID "(" parametros ")" "{" statement retorno ";" "}"')
    def funcion(self, p):
        return ("funcion", p.TYPE, p.ID, p.parametros, p.statement)

    @_('VOID ID "(" parametros ")" "{" statement "}"')
    def funcion(self, p):
        return ("funcion", p.VOID, p.ID, p.parametros, p.statement)

    @_('')
    def funciones(self, p):
        return []

    @_('parametros "," TYPE ID')
    def parametros(self, p):
        return ("parametros", p.TYPE, p.ID)

    @_('TYPE ID')
    def parametros(self, p):
        #self.anadir_variable(p.TYPE, p.ID)
        return (p.TYPE, p.ID)

    @_('')
    def parametros(self, p):
        pass

    @_('RETURN expr')
    def retorno(self, p):
        return ("return", p.expr)

    # Statement
    @_('defi_list expr_list')
    def statement(self, p):
        return (p.defi_list, p.expr_list)

    @_('defi_list')
    def statement(self, p):
        return (p.defi_list, [])

    @_('expr_list')
    def statement(self, p):
        return ([], p.expr_list)

    @_('')
    def statement(self, p):
        pass

    # def_list (lista de definiciones, permite múltiples declaraciones)

    @_('defi_list defi ";"')
    def defi_list(self, p):
        return p.defi_list + [p.defi]

    # Caso vacío
    # @_('')
    # def defi_list(self, p):
    #    return []

    @_('defi ";"')
    def defi_list(self, p):
        return p.defi

    # def (declaración individual)
    @_('TYPE id_list')
    def defi(self, p):
        #for id in p.id_list:
        #    self.anadir_variable(p.TYPE, id)
        return [(p.TYPE, id) for id in p.id_list]

    # def (declaración individual)
    # @_('TYPE expr')
    # def defi(self, p):
    #    lvalues = [item[1] for item in p.expr if item[0] == 'assign']
    #    for id in lvalues:
    #        self.anadir_variable(p.TYPE, id)
    #    return (p.TYPE, p.expr)

    @_('declaracion_variables')
    def defi(self, p):
        return ("defi", p.declaracion_variables)

    @_('TYPE expr_mult')
    def declaracion_variables(self, p):
        '''
        lvalues = []

        if type(p.expr_mult[0]) == tuple:  # hay varias assigns
            for p2 in p.expr_mult:
                # print(p2)
                if p2[0] == 'assign':
                    lvalues.append(p2[1])  # METER IDS EN LVALUES
        else:
            if p.expr_mult[0] == 'assign':
                lvalues.append(p.expr_mult[1])  # METER IDS EN LVALUES
            # lvalues.append(p2[1])#METER IDS EN LVALUES

        #  print("lvalores = ",lvalues)#PRINT PARA DEBUG
        for lv in lvalues:

            self.anadir_variable(p.TYPE, lv)'''

        return ("expr_mult", p.TYPE, p.expr_mult)

    @_('expr_mult "," expr')
    def expr_mult(self, p):
        return (p.expr_mult, p.expr)

    @_('expr')
    def expr_mult(self, p):
        return p.expr

    # Lista de identificadores separados por comas

    @_('ID')
    def id_list(self, p):
        return [p.ID]

    @_('id_list "," ID')
    def id_list(self, p):
        return [p.ID] + p.id_list

    # @_('ID "," id_list')
    # def id_list(self, p):
        # return [p.ID] + p.id_list

    # @_('ID')
    # def id_list(self, p):
        # return [p.ID]

    # expr_list

    @_('expr_list expr ";"')
    def expr_list(self, p):
        return p.expr_list + [p.expr]

    # @_('')
    # def expr_list(self, p):
    #    return []

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

    @_('opUn opUnT')
    def opUn(self, p):
        return p.opUn * p.opUnT

    @_('opUnT')
    def opUn(self, p):
        return p.opUnT

    # @_('opUn NOT')
    # def opUn(self, p):
    #    return not p.opUn

    @_('NOT')
    def opUnT(self, p):
        return False

    @_('MINUS')
    def opUnT(self, p):
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

    '''
    textos = {"int x <= 8;", "a = b + c;", "a = 6 - 2;", "a = !b != c;",
              "a == c;", "a = b*c/d = 56;", "; ; ;",
              "int f; int o; int c;", "int m;", "int j, k, l;", "int s = 3;",
              "int a = 3; int b = 5;", "int r = 6, q = 7;", "void aa;",
              "int a(int x) {};"
              }
    '''

    textos = {'''
              int g1,g2;


              int main(int a, int b) { a == c; return a; }
              void x() { int b;  }
              void y() {}
              void y(int a){}'''
              }

    for texto in textos:
        try:
            print("\n\n\n\n", texto, " :")
            tokens = lexer.tokenize(texto)
            result = parser.parse(tokens)
            print(result)
        except Exception as err:
            print(f"Error de compilación: {err}")

    print("tabla de simbolos :")

    for clave, valor in parser.simbolos.items():

        print(type(valor), " ", clave, " = ", valor)
