from sly import Parser
from CLexer import CLexer
from clasesnodos import *
from collections import deque
import asm_translator


class CParser(Parser):
    # lexer
    tokens = CLexer.tokens
    debugfile = 'parser.out'
    simbolos = dict()
    asm = ""
    contadoretiquetas = 0

    precedence = (
        ('right', ASSIGN),
        ('left', OR),
        ('left', AND),
        ('left', EQ, NE, LE, GE),
        ('left', PLUS, MINUS),
        ('left', MULTIPLY, DIVIDE),
        ('right', NOT),
        ('left', '['),
    )

    ###########################################################################
    ##################### FUNCIONES AUXILIARES ################################
    ###########################################################################

    def anadir_simbolo(self, tipo, nombre, contenido=0, globales=[]):
        if isinstance(nombre, list):
            for n in nombre:
                self.anadir_simbolo_individual(tipo, n, contenido)
        else:
            self.anadir_simbolo_individual(tipo, nombre, contenido)

    def anadir_simbolo_individual(self, tipo, nombre, contenido=0):
        try:
            if nombre not in self.simbolos:
                if tipo == "int" or tipo == "funcion" or tipo == "int* ":
                    self.simbolos[nombre] = contenido
                else:
                    raise Exception("tipo no valido")
            else:
                raise Exception(
                    f"variable {nombre} ya declarada anteriormente")
        except Exception:
            pass

   
    def push_asm(self, str):
        self.asm += "\n" + str

    ###########################################################################
    # -------------------------------------------------------------------------
    # -------------------- FIN DE FUNCIONES AUXILIARES ------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ################################ S ########################################
    ###########################################################################

    '''
    @_('globales "$" funciones')
    def S(self, p):
        for g in p.globales:
            punt = ""
            if g.espuntero:
                punt = "* "
            #print(g)
            # print(g)
            self.anadir_simbolo(g.tipo + punt, punt + g.nombre + str(g.array))
            self.push_asm(f".globl {g.nombre}")

        for f in p.funciones:
            #print("Funcion : \n\n ",f,"\n\n")
            self.anadir_simbolo(f.tipo,f.nombre,f.cuerpo)

            #empujar codigo de la funciion
            self.push_asm(f.ensamblador)

        #print("\nASM\n===================================================\n\n")
        #print(self.asm)

        with open("asm.txt", "w") as archivo:
            archivo.write(self.asm)

       # print("\n\nFIN ASM\n==========================================================\n")

        return (p.globales, p.funciones)
    '''
    
    @_('globales "$" funciones')
    def S(self, p):
        print(p.globales)
        if isinstance(p.globales, list):
            for g in p.globales:
                punt = ""
                if g.espuntero:
                    punt = "* "
                # Añadir símbolo y ensamblador
                self.anadir_simbolo(g.tipo + punt, punt + g.nombre + str(g.array))
                self.push_asm(f".globl {g.nombre}")
        else:
            if p.globales:
                g = p.globales
                punt = ""
                if g.espuntero:
                    punt = "* "
                # Añadir símbolo y ensamblador
                self.anadir_simbolo(g.tipo + punt, punt + g.nombre + str(g.array))
                self.push_asm(f".globl {g.nombre}")

        # Verificar y procesar `p.funciones`
        if isinstance(p.funciones, list):
            for f in p.funciones:
                # Añadir símbolo y ensamblador
                self.anadir_simbolo(f.tipo, f.nombre, f.cuerpo)
                textos_globales = [""]
                self.push_asm(f.cadena(textos_globales))
                self.asm = "".join(textos_globales) + self.asm
                
        else:
            f = p.funciones
            # Añadir símbolo y ensamblador
            self.anadir_simbolo(f.tipo, f.nombre, f.cuerpo)
            textos_globales = []
            self.push_asm(f.cadena(textos_globales))
           
            self.asm = "".join(textos_globales) + self.asm
        # Guardar ensamblador en archivo
        with open("asm.txt", "w") as archivo:
            archivo.write(self.asm)

        return (p.globales, p.funciones)

    
    ###########################################################################
    # -------------------------------------------------------------------------
    # -------------------------- FIN_S ----------------------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ############################ GLOBALES #####################################
    ###########################################################################

    @_('defi_list')
    def globales(self, p):
        return p.defi_list

    @_('')
    def globales(self, p):
        return None

    ###########################################################################
    # -------------------------------------------------------------------------
    # ------------------------- FIN_GLOBALES ----------------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ############################ FUNCIONES ####################################
    ###########################################################################

    @_('funciones funcion')
    def funciones(self, p):
        return p.funciones + [p.funcion]

    @_('TYPE ID "(" parametros ")" "{" statement retorno ";" "}"')
    def funcion(self, p):

        return nodofuncion(p.TYPE, p.ID, p.parametros, p.statement,self.contadoretiquetas, p.retorno)
        #return ("funcion", p.TYPE, p.ID, p.parametros, p.statement)

    @_('VOID ID "(" parametros ")" "{" statement "}"')
    def funcion(self, p):

        return nodofuncion(p.VOID, p.ID,p.parametros,p.statement,self.contadoretiquetas)
        # return ("funcion", p.VOID, p.ID, p.parametros, p.statement)

    @_('')
    def funciones(self, p):
        return []

    ###########################################################################
    # -------------------------------------------------------------------------
    # ------------------------- FIN_FUNCIONES ---------------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ############################ PARÁMETROS ###################################
    ###########################################################################

    @_('parametros "," TYPE ID')
    def parametros(self, p):
        return  p.parametros + [(p.TYPE, p.ID)]

    @_('TYPE ID')
    def parametros(self, p):
        return [(p.TYPE, p.ID)]

    @_('parametros "," TYPE MULTIPLY ID')
    def parametros(self, p):
        
        return  p.parametros + [(('*', p.TYPE), p.ID)]

    @_('TYPE MULTIPLY ID')
    def parametros(self, p):
        #print(p.ID,"sdijahndsaidhsa")
        return [(('*', p.TYPE), p.ID)]

    @_('')
    def parametros(self, p):
        return []

    @_('RETURN operacion')
    def retorno(self, p):

        

        
        return nodoreturn(p.operacion,self.contadoretiquetas)

    ###########################################################################
    # -------------------------------------------------------------------------
    # ---------------------------- FIN_PARÁMETROS -----------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ############################# STATEMENT ###################################
    ###########################################################################

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

    ###########################################################################
    # -------------------------------------------------------------------------
    # ---------------------------- FIN_STATEMENT ------------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ################################ DEFI_LIST ################################
    ###########################################################################

    @_('defi_list defi ";"')
    def defi_list(self, p):
        if not isinstance(p.defi_list, list):
            defi_list = [p.defi_list]
        else:
            defi_list = p.defi_list

        if not isinstance(p.defi, list):
            defi = [p.defi]
        else:
            defi = p.defi

        return defi_list + defi

    @_('defi ";"')
    def defi_list(self, p):
        return p.defi

    ###########################################################################
    # -------------------------------------------------------------------------
    # ---------------------------- FIN_DEFI_LIST ------------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ################################### DEFI ##################################
    ###########################################################################

    @_('TYPE id_list')
    def defi(self, p):

        if isinstance(p.id_list, list):
            for d in p.id_list:  # PONER TIPO
                d.tipo = p.TYPE

        else:
            p.id_list.tipo = p.TYPE

        return p.id_list

    @_('declaracion_variables')
    def defi(self, p):
        return ("defi", p.declaracion_variables)

    @_('TYPE expr_mult')
    def declaracion_variables(self, p):
        return ("expr_mult", p.TYPE, p.expr_mult)

    @_('expr_mult "," expr')
    def expr_mult(self, p):
        return (p.expr_mult, p.expr)

    @_('expr')
    def expr_mult(self, p):
        return p.expr

    # Lista de identificadores separados por comas

    ###########################################################################
    # -------------------------------------------------------------------------
    # -------------------------------- FIN_DEFI -------------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ############################### ID_LIST ###################################
    ###########################################################################

    @_('id_list "," id_array')
    def id_list(self, p):
        if isinstance(p.id_list, list):
            return p.id_list + [p.id_array]
        else:
            return [p.id_list] + [p.id_array]

    '''
    @_('ID')
    def id_list(self, p):
        return [p.ID]
    '''

    @_('id_array')
    def id_list(self, p):

        return p.id_array

    ###########################################################################
    # -------------------------------------------------------------------------
    # ----------------------------- FIN_ID_LIST -------------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ################################# ARRAY ###################################
    ###########################################################################

    @_('MULTIPLY id_array')  # PUNTERO
    def id_array(self, p):
        p.id_array.espuntero = True

        return p.id_array

    @_('ID')
    def id_array(self, p):

        return Nododeclaracion(p.ID, "int", False, [1])

    @_('ID array')
    def id_array(self, p):

        return Nododeclaracion(p.ID, "int", False, p.array)

    @_('array "[" NUMBER "]"')
    def array(self, p):

        return p.array + [int(p.NUMBER)]

    @_('"[" NUMBER "]"')
    def array(self, p):

        return [int(p.NUMBER)]

    ###########################################################################
    # -------------------------------------------------------------------------
    # ----------------------------- FIN_ARRAY ---------------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ############################### EXPR_LIST #################################
    ###########################################################################

    @_('expr_list expr ";"')
    def expr_list(self, p):

        if (not isinstance(p.expr_list, list)):
            return [p.expr_list] + [p.expr]

        return p.expr_list + [p.expr]

    @_('expr ";"')
    def expr_list(self, p):
        return [p.expr]

    ###########################################################################
    # -------------------------------------------------------------------------
    # ---------------------------- FIN_EXPR_LIST ------------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ################################## EXPR ###################################
    ###########################################################################

    @_('lvalue ASSIGN operacion')
    def expr(self, p):

        return Nodoasignacion(p.operacion, p.lvalue,self.contadoretiquetas)

    @_('operacion')
    def expr(self, p):
        
        return p.operacion

    @_('lvalue ASSIGN ID')
    def lvalue(self, p):


        return p.lvalue + [p.ID]
        

    @_('ID')
    def lvalue(self, p):
        return [p.ID]

    @_('"*" ID')
    def lvalue(self, p):
        return [('*', p.ID)]

    ###########################################################################
    # -------------------------------------------------------------------------
    # ------------------------------ FIN_EXPR ---------------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ################################## PRINTF #################################
    ###########################################################################

    @_('PRINTF "(" printf_args ")"')
    def expr(self, p):
        return Nodoprint(p.printf_args)

    @_('STRING "," variables_a_imprimir')
    def printf_args(self, p):

        # ¡¡¡ NO ELIMINAR ESTE BLOQUE DE CÓDIGO COMENTADO !!!
        '''
        texto = p.STRING[1:-1]  # Elimina las comillas dobles de los extremos

        # Detectar y procesar especificadores de formato
        especificadores_formato = re.findall(r'%[diufFeEgGxXoscp]', texto)
        print("Especificadores formato detectados:", especificadores_formato)
        num_especificadores = len(especificadores_formato)
        print("Num de especif. form. detectados:", num_especificadores)
        num_variables_a_imprimir = len(p.variables_a_imprimir[0])
        print(p.variables_a_imprimir)
        print("Num de variables a imprimir:", num_variables_a_imprimir)

        if (num_especificadores != num_variables_a_imprimir):
            raise Exception(
                "El número de especificadores de formato y el número de variables a imprimir son distintos.")
        if(num_especificadores != num_variables_a_imprimir):
            raise Exception(
                "El número de especificadores de formato y el número de variables a imprimir son distintos.")
        '''

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

    @_('id_list')
    def variables_a_imprimir(self, p):
        if isinstance(p.id_list, tuple):
            return list(p.id_list)
        else:
            return p.id_list

    @_('operaciones_a_imprimir "," operacion')
    def operaciones_a_imprimir(self, p):
        if isinstance(p.operaciones_a_imprimir, tuple):
            return list(p.operaciones_a_imprimir) + [p.operacion]
        else:
            return [p.operaciones_a_imprimir] + [p.operacion]

    @_('operacion')
    def operaciones_a_imprimir(self, p):

        return p.operacion

    ###########################################################################
    # -------------------------------------------------------------------------
    # -------------------------- PRINTF_FIN -----------------------------------
    # -------------------------------------------------------------------------
    ###########################################################################

    ###########################################################################
    ############################### SCANF #####################################
    ###########################################################################

    @_('SCANF "(" scanf_args ")"')
    def expr(self, p):
        return ("scanf", p.scanf_args)

    @_('STRING "," variables_referenciadas')
    def scanf_args(self, p):
        return (p.STRING, p.variables_referenciadas)

    @_('variables_referenciadas "," "&" ID')
    def variables_referenciadas(self, p):
        return (p.variables_referenciadas, ('&', p.ID))

    @_('"&" ID')
    def variables_referenciadas(self, p):
        return (p.ID)

    # -------------------------------------------------------------------------
    # ------------------------------ SCANF_FIN --------------------------------
    # -------------------------------------------------------------------------

    ###########################################################################
    ############################### IF_ELSE ###################################
    ###########################################################################

    @_('expr_list block_expr')
    def expr_list(self, p):
        return (p.expr_list, p.block_expr)

    @_('block_expr')
    def expr_list(self, p):
        return (p.block_expr)

    @_('IF "(" operacion ")" "{" expr_list "}" cont_cond')
    def block_expr(self, p):
        return NodoIF(p.operacion,p.expr_list,p.cont_cond,self.contadoretiquetas)

    @_('ELSE "{" expr_list "}"')
    def cont_cond(self, p):
        return p.expr_list

    @_('')
    def cont_cond(self, p):
        return None

    ###########################################################################
    # -------------------------------------------------------------------------
    # ----------------------------- IF_ELSE_FIN -------------------------------
    # -------------------------------------------------------------------------
    ###########################################################################
    

    ###########################################################################
    ################################ WHILE_LOOP ###############################
    ###########################################################################

    @_('WHILE "(" operacion ")" "{" expr_list "}"')
    def block_expr(self, p):
        
        return NodoWhile( p.operacion, p.expr_list , self.contadoretiquetas)
    
    ###########################################################################
    # -------------------------------------------------------------------------
    # ----------------------------- WHILE_LOOP_FIN ----------------------------
    # -------------------------------------------------------------------------
    ###########################################################################



    ###########################################################################
    ################################ OPERACIONES ##############################
    ###########################################################################

    @_('opLogOr')
    def operacion(self, p):
        return p.opLogOr
    
    # opLogOr
    @_('opLogOr OR opLogAnd')
    def opLogOr(self, p):
        return NodoOr(p.opLogOr, p.opLogAnd,self.contadoretiquetas,"||")

    @_('opLogAnd')
    def opLogOr(self, p):
        return p.opLogAnd

    # opLogAnd
    @_('opLogAnd AND opUnario')
    def opLogAnd(self, p):
        return NodoAnd(p.opLogAnd, p.opUnario,self.contadoretiquetas,"&&")

    @_('opUnario')
    def opLogAnd(self, p):
        # pila = deque()
        # self.bajar_arbo(p.opUnario,pila)
       # while pila:
        #    pila.pop().escribe()

        # print("-------------------")
        return p.opUnario

    

    @_('opUn opComp')
    def opUnario(self, p):
        return NodoopUnario(p.opUn, p.opComp,self.contadoretiquetas)
    
    @_('NOT')
    def opUn(self, p):
        return '!'

    @_('MINUS')
    def opUn(self, p):
        return '-'

    @_('opComp')
    def opUnario(self, p):
        return p.opComp
    # -------------------------------------------------------------------------

    # Operaciones de comparación
    
    @_('opComp EQ opSumaResta')
    def opComp(self, p):
        return NodoOpComp(p.opComp, '==', p.opSumaResta)

    @_('opComp NE opSumaResta')
    def opComp(self, p):
        return NodoOpComp(p.opComp, '!=', p.opSumaResta)

    @_('opComp LE opSumaResta')
    def opComp(self, p):
        return NodoOpComp(p.opComp, '<=', p.opSumaResta)

    @_('opComp GE opSumaResta')
    def opComp(self, p):
        return NodoOpComp(p.opComp, '>=', p.opSumaResta)

    @_('opSumaResta')
    def opComp(self, p):
        return p.opSumaResta
    
    # -------------------------------------------------------------------------
    
    # opSumaResta
    @_('opSumaResta PLUS opMultDiv')
    def opSumaResta(self, p):
        return Nodosumaresta(p.opSumaResta, '+', p.opMultDiv)

    @_('opSumaResta MINUS opMultDiv')
    def opSumaResta(self, p):
        return Nodosumaresta(p.opSumaResta, '-', p.opMultDiv)

    @_('opMultDiv')
    def opSumaResta(self, p):
        return p.opMultDiv

    # opMultDiv
    @_('opMultDiv MULTIPLY term')
    def opMultDiv(self, p):
        # print("soy una suma ")
        return NodoMultDiv(p.opMultDiv, "*", p.term)

    @_('opMultDiv DIVIDE term')
    def opMultDiv(self, p):
        return NodoMultDiv(p.opMultDiv, "/", p.term)

    @_('term')
    def opMultDiv(self, p):
        return p.term

    # term rules (variables or numbers)
    @_('ID')
    def term(self, p):
        print(p.ID)
        return Nodotermino(p.ID)

    @_('NUMBER')
    def term(self, p):
        # print("soy un numero")
        return Nodotermino(p.NUMBER)

    @_('"*" ID')
    def term(self, p):
        return Nodotermino(p.ID, '*')

    @_('"&" ID')
    def term(self, p):
        return Nodotermino(p.ID, '&')

    @_('ID "[" term "]"')
    def term(self, p):
        return Nodotermino(p.ID, 'a', p.term)

    @_('"(" expr ")"')
    def term(self, p):
        return p.expr


###########################################################################
# -------------------------------------------------------------------------
# -------------------------- FIN_OPERACIONES ------------------------------
# -------------------------------------------------------------------------
###########################################################################


global tabla
tabla = []


###########################################################################
################################## Main ###################################
###########################################################################

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
              int g1, g2 ,*g3;

              int funcion1(int a){
                a = b;
              return 1;
              }
            
              int main(int *a, int b , int c) {
                int bc[12][43];
              int cb;
                    
                    g1 = 5*a1 + a2/10 - a3 * a4 - 15;
                    g2 = g1 = c = b;
                  return 1;
              }
                '''
              }
    for texto in textos:
        # try:
        print("\n\n\n\n", texto, " :")
        tokens = lexer.tokenize(texto)
        result = parser.parse(tokens)
        #print(result)

        # except Exception as err:
        # print(f"Error de compilación: {err}")

    print("tabla de simbolos :")

    for clave, valor in parser.simbolos.items():
        pass
        #print(type(valor), " ", clave, " = ", valor)


###########################################################################
# -------------------------------------------------------------------------
# ----------------------------- FIN_MAIN ----------------------------------
# -------------------------------------------------------------------------
###########################################################################
