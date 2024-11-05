from sly import Parser
from CLexer import CLexer
from clasesnodos import *
import re

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

    ###########################################################################
    ##################### FUNCIONES AUXILIARES ################################
    ###########################################################################

    def anadir_simbolo(self, tipo, nombre, contenido=0):
        if isinstance(nombre, list):
            for n in nombre:
                self.anadir_simbolo_individual(tipo, n, contenido)
        else:
            self.anadir_simbolo_individual(tipo, nombre, contenido)

    def anadir_simbolo_individual(self, tipo, nombre, contenido=0):
        if nombre not in self.simbolos:
            if tipo == "int" or tipo == "funcion":
                self.simbolos[nombre] = contenido
            else:
                raise Exception("tipo no valido")
        else:
            raise Exception(f"variable {nombre} ya declarada anteriormente")

    
    '''
    def anadir_simbolo(self, tipo, nombre , contenido = 0):

        if nombre not in self.simbolos:
vv
            if tipo == "int":
                self.simbolos[nombre] = contenido
            elif tipo == "funcion":
                self.simbolos[nombre] = contenido
            else:
                raise Exception("tipo no valido")

        else:

            raise Exception("variable ", nombre, " ya declarada anteriormente")
    '''

    #--------------------------------------------------------------------------
    #-------------------- FIN DE FUNCIONES AUXILIARES -------------------------
    #--------------------------------------------------------------------------

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

    #############################################################
    ##################### ID_LIST ###############################
    #############################################################

    @_('ID')
    def id_list(self, p):
        return [p.ID]

    @_('id_list "," ID')
    def id_list(self, p):
        if isinstance(p.id_list, tuple):
            return list(p.id_list) + [p.ID]
        else:
            return [p.id_list] + [p.ID]
        
        #return [p.ID] + p.id_list

    # @_('ID "," id_list')
    # def id_list(self, p):
        # return [p.ID] + p.id_list

    # @_('ID')
    # def id_list(self, p):
        # return [p.ID]

    #------------------------------------------------------------
    #-------------------- FIN DE ID_LIST ------------------------
    #------------------------------------------------------------

    # expr_list

    @_('expr_list expr ";"')
    def expr_list(self, p):
        return p.expr_list + [p.expr]

    # @_('')
    # def expr_list(self, p):
    #    return []

    @_('expr ";"')
    def expr_list(self, p):
        return [('expr', p.expr)]

    # expr

    @_('lvalue ASSIGN opComp')
    def expr(self, p):
        return ('assign', p.lvalue, p.opComp)

    ##########################################################
    ################### PRINTF ###############################
    ##########################################################

    @_('PRINTF "(" printf_args ")"')
    def expr(self, p):
        return ("printf", p.printf_args)

    @_('STRING "," variables_a_imprimir')
    def printf_args(self, p):
        print("Cadena:", p.STRING)
        
        texto = p.STRING[1:-1]  # Elimina las comillas dobles de los extremos

        # Detectar y procesar especificadores de formato
        especificadores_formato = re.findall(r'%[diufFeEgGxXoscp]', texto)
        print("Especificadores formato detectados:", especificadores_formato)
        num_especificadores = len(especificadores_formato)
        print("Num de especif. form. detectados:", num_especificadores)
        num_variables_a_imprimir = len(p.variables_a_imprimir)
        print("Num de variables a imprimir:", num_variables_a_imprimir)

        if(num_especificadores != num_variables_a_imprimir):
            raise Exception("El número de especificadores de formato y el número de variables a imprimir son distintos.")

        return (p.STRING, p.variables_a_imprimir)

    @_('STRING')
    def printf_args(self, p):
        return p.STRING

    @_('operaciones_a_imprimir')
    def variables_a_imprimir(self, p):
        if isinstance(p.operaciones_a_imprimir, tuple):
            return list(p.operaciones_a_imprimir)
        else:
            return [p.operaciones_a_imprimir]

        # return p.operaciones_a_imprimir

    @_('id_list')
    def variables_a_imprimir(self, p):
        if isinstance(p.id_list, tuple):
            return list(p.id_list)
        else:
            return [p.id_list]
        
        # return p.id_list

    @_('operaciones_a_imprimir "," opComp')
    def operaciones_a_imprimir(self, p):
        if isinstance(p.operaciones_a_imprimir, tuple):
            return list(p.operaciones_a_imprimir) + [p.opComp]
        else:
            return [p.operaciones_a_imprimir] + [p.opComp]
        
        # return (p.operaciones_a_imprimir, p.opComp)

    @_('opComp')
    def operaciones_a_imprimir(self, p):
        return [p.opComp]

        # return p.opComp

    #---------------------------------------------------------
    #------------------ PRINTF_FIN ---------------------------
    #---------------------------------------------------------

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
    ##########################################################
    ################### OP_COMPARACIÓN #######################
    ##########################################################

    '''
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
    '''

    @_('opComp EQ opLogOr')
    def opComp(self, p):
        return NodoOpComp(p.opComp, '==', p.opLogOr)

    @_('opComp NE opLogOr')
    def opComp(self, p):
        return NodoOpComp(p.opComp, '!=', p.opLogOr)

    @_('opComp LE opLogOr')
    def opComp(self, p):
        return NodoOpComp(p.opComp, '<=', p.opLogOr)

    @_('opComp GE opLogOr')
    def opComp(self, p):
        return NodoOpComp(p.opComp, '>=', p.opLogOr)

    @_('opLogOr')
    def opComp(self, p):
        return p.opLogOr

    #---------------------------------------------------------
    #--------------- OP COMPARACIÓN_FIN ----------------------
    #---------------------------------------------------------

    # opLogOr
    @_('opLogOr OR opLogAnd')
    def opLogOr(self, p):
        return NodoopLogOr(p.opLogOr, p.opLogAnd)

    @_('opLogAnd')
    def opLogOr(self, p):
        return p.opLogAnd

    # opLogAnd
    @_('opLogAnd AND opUnario')
    def opLogAnd(self, p):
        return NodoopLogAnd(p.opLogAnd, p.opUnario)

    

    @_('opUnario')
    def opLogAnd(self, p):
        return p.opUnario
    
    # opUnario
    @_('opUn opMultDiv')
    def opUnario(self, p):
        return NodoopUnario(p.opUn,p.opMultDiv)


    # @_('opUn NOT')
    # def opUn(self, p):
    #    return not p.opUn

    @_('NOT')
    def opUn(self, p):
        return '!'

    @_('MINUS')
    def opUn(self, p):
        return '-'

    # opMultDiv

    @_('opMultDiv')
    def opUnario(self, p):
        return p.opMultDiv

    # opMultDiv
    @_('opMultDiv MULTIPLY opSumaResta')
    def opMultDiv(self, p):
        return NodoMultDiv(p.opMultDiv,'*', p.opSumaResta)

    @_('opMultDiv DIVIDE opSumaResta')
    def opMultDiv(self, p):
        return NodoMultDiv( p.opMultDiv,'/',p.opSumaResta)

    @_('opSumaResta')
    def opMultDiv(self, p):
        return p.opSumaResta

    # opSumaResta
    @_('opSumaResta PLUS term')
    def opSumaResta(self, p):
        # print("soy una suma ")
         return Nodosumaresta(p.opSumaResta,"+", p.term)

    @_('opSumaResta MINUS term')
    def opSumaResta(self, p):
        return Nodosumaresta(p.opSumaResta,"-", p.term)

    @_('term')
    def opSumaResta(self, p):
        return p.term

    # term rules (variables or numbers)
    @_('ID')
    def term(self, p):
        
        return Nodotermino(p.ID)

    @_('NUMBER')
    def term(self, p):
        # print("soy un numero")
        return Nodotermino(p.NUMBER)


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

    # prueba a poner printf("Hola"); despues de a==c;
    
    textos = {'''
              int g1, g2;


              int main(int a, int b) { a+c ;printf("hola"); return 1; }
              void x() { int b; }
              void y(int a){}'''
              }
              

    for texto in textos:
        #try:
            print("\n\n\n\n", texto, " :")
            tokens = lexer.tokenize(texto)
            result = parser.parse(tokens)
            print(result)
        #except Exception as err:
            #print(f"Error de compilación: {err}")

    print("tabla de simbolos :")

    for clave, valor in parser.simbolos.items():

        print(type(valor), " ", clave, " = ", valor)
