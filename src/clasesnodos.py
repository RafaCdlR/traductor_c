class Nodo():

    def cadena(self):
        return ""

    def escribe(self):
        pass

    def __str__(self):

        return self.cadena()

    def __repr__(self):
        return self.cadena()
    

class nodoreturn(Nodo):
    def __init__(self,cad , esoperacion = False):
        self.cad = cad
        self.esoperacion = esoperacion
    def cadena(self):
        cad = ""
        if self.cad != "":#si la cadena esta vacia es un void y solo se hace la parte final
                
            
            if self.esoperacion:
                cad = self.cad + f"mov1 $eax$ ${cad}$\n"
            else:
                cad = f"mov1 ${self.cad}$ $eax$\n"

        return cad + "movl %ebp, %esp  \npopl %ebp \nret  \n"



class nodofuncion(Nodo):
    

    #pushear ebp(base antes de la funcion)
    #luego copiar esp a ebp
    #al final volver a copiar la primera posicion de la base de la pila a ebp (base anterior) (ret)

    def __init__(self,tipo,nombre, parametros , cuerpo , retorno = nodoreturn("")):
        pila = dict()
        self.tipo = tipo
        self.nombre = nombre
        self.parametros = parametros
        self.cuerpo =  cuerpo
        
        self.ensamblador = f'''
.text \n 
.globl {nombre} \n 
.type {nombre}, @function \n 
{nombre}:  \n 
pushl %ebp \n 
movl %esp, %ebp\n'''

        contador = 0
        print("funcion : ",nombre,"\n\n")
        for var in parametros:
            print(var[1])

            if var[1] in pila:#MANEJO DE ERRORES
                
                raise ValueError(f"Error: variable repetida {var[1]} en la función {nombre}")
            


            pila[var[1]] = f"{contador}(%ebp)"
            
            contador += 4

        #restar la memoria de los parametros:
        self.ensamblador += f"subl ${contador} %esp\n"

        #declaraciones 
        for ins in self.cuerpo[0]:

            if isinstance(ins,Nodo):
                self.ensamblador += ins.cadena()
            else:
                self.ensamblador += f"\n FALTA NODO : {ins} \n"
        

        #instrucciones
        for ins in self.cuerpo[1]:

            self.ensamblador += "\n#" +type(ins).__name__+ "\n\n"
            if isinstance(ins,Nodo):
                self.ensamblador += ins.cadena()
            else:
                self.ensamblador += f"\n FALTA NODO : {ins} \n"
            





        self.ensamblador += "\n# el return : \n\n"#comentario del return

        #final el return
        self.ensamblador += retorno.cadena()

        
        print("\n\nfin funcion",nombre)




    def cadena(self):
        return f"{self.nombre}( {self.parametros} )" + "{ " + f" {self.cuerpo} " + " }\n"  # devuelve cadena a imprimir
    def escribe(self):
        print(self.cadena())


class Nodotermino(Nodo):
    valor = None  # valor numerico

    def __init__(self, v, simbolo=None, offset=None):
        if (simbolo == '*'):
            self.valor = v
            self.desreferencia = True
        elif (simbolo == '&'):
            self.valor = v
            self.desreferencia = False
        elif (simbolo == 'a'):
            self.valor = v
            self.desreferencia = True
            self.desplazamiento = offset
        else:
            self.valor = v
            self.desreferencia = False

    def cadena(self):
        return f"{self.valor}"  # devuelve cadena a imprimir

    def escribe(self):
        print(self.cadena())


class Nodosumaresta(Nodo):
    left = ""
    right = ""
    operador = ""

    def __init__(self, left, operador="", right=""):

        self.left = left
        self.right = right
        self.operador = operador

    def cadena(self):
        return f"{self.left.cadena()}{self.operador}{self.right.cadena()}"

    def escribe(self):
        print(self.cadena())


class NodoMultDiv(Nodo):
    left = ""
    right = ""
    operador = ""

    def __init__(self, left, operador="", right=""):

        self.left = left
        self.right = right
        self.operador = operador

    def cadena(self):
        return f"{self.left.cadena()}{self.operador}{self.right.cadena()}"

    def escribe(self):
        print(self.cadena())


'''
class NodoopUn(Nodo):
    operador = ""
    def __init__(self,operador):
        assert(operador == "-" or operador == "!")
        self.operador = operador

    def cadena(self):
        return f"{self.operador}"
    
    def escribe(self):
        print(self.cadena())
'''


class NodoopUnario(Nodo):
    operador = ""
    right = ""

    def __init__(self, operador, right):

        self.operador = operador
        self.right = right

    def cadena(self):
        return f"{self.operador.cadena()}{self.right.cadena()}"

    def escribe(self):
        print(self.cadena())


class NodoopLogAnd(Nodo):
    operador = "&&"
    right = ""
    left = ""

    def __init__(self, left, right):

        self.left = left
        self.right = right

    def cadena(self):
        return f"{self.left.cadena()}{self.operador}{self.right.cadena()}"

    def escribe(self):
        print(self.cadena())


class NodoopLogOr(Nodo):
    operador = "||"
    right = ""
    left = ""

    def __init__(self, left, right):

        self.left = left
        self.right = right

    def cadena(self):
        return f"{self.left.cadena()}{self.operador}{self.right.cadena()}"

    def escribe(self):
        print(self.cadena())


class NodoOpComp(Nodo):

    def __init__(self, left, op, right):
        self.left = left
        self.operador = op
        self.right = right

    def cadena(self):
        return f"{self.left.cadena()}{self.operador}{self.right.cadena()}"

    def escribe(self):
        print(self.cadena())


class Nododeclaracion(Nodo):

    def __init__(self, nombre, tipo, espuntero=False, array=[]):
        self.nombre = nombre
        self.tipo = tipo
        self.espuntero = espuntero
        self.array = array

    def cadena(self):
        p = ""
        if self.espuntero:
            p = "* "

        return f"{self.tipo}{p} {self.nombre} {self.array}"

    def escribe(self):
        print(self.cadena())

class Nodoasignacion(Nodo):
    #dest = origen;
    def __init__(self, orig , dest , esoperacion):
        self.dest = dest
        self.orig = orig
        self.esoperacion = esoperacion

    def cadena(self):
        
        if self.esoperacion:
            cad = self.orig + f"mov1 $eax$ ${self.dest[-1]}$\n"
        else:
            cad = f"mov1 ${self.orig}$ ${self.dest[-1]}$\n"



        ant = self.dest[-1]
        for id  in self.dest[-2::-1]:
            cad += f"mov1 ${ant}$ ${id}$\n"
            ant = id


        return cad

    def escribe(self):
        print(self.cadena())





class Nodocadena(Nodo):
    def __init__(self, nombre):
        self.nombre = nombre

    def cadena(self):
        return self.nombre
