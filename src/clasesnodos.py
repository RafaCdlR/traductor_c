class Nodo():
    
    def cadena(self):
        return ""
    
    def escribe(self):
        pass

    def __str__(self):
        
        return self.cadena()
    
    def __repr__(self):
        return self.cadena()



class Nodotermino(Nodo):
    valor = None #valor numerico
    def __init__(self, v, simbolo=None, offset=None):
        if(simbolo == '*'):
            self.valor = v
            self.desreferencia = True
        elif(simbolo == '&'):
            self.valor = v
            self.desreferencia = False
        elif(simbolo == 'a'):
            self.valor = v
            self.desreferencia = True
            self.desplazamiento = offset
        else:
            self.valor = v
            self.desreferencia = False


    def cadena(self):
        return f"{self.valor}" # devuelve cadena a imprimir

    def escribe(self):
        print(self.cadena())



class Nodosumaresta(Nodo):
    left = ""
    right = ""
    operador = ""

    def __init__(self , left, operador ="" , right =""  ):
        
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

    def __init__(self , left  , operador ="", right =""   ):
        
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

    def __init__(self,operador,right):
        
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
    def __init__(self,left,right):
        
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
    def __init__(self,left,right):
        
        self.left = left
        self.right = right

    def cadena(self):
        return f"{self.left.cadena()}{self.operador}{self.right.cadena()}"
    
    def escribe(self):
        print(self.cadena())





class NodoOpComp(Nodo):

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def cadena(self):
        return f"{self.left.cadena()}{self.op}{self.right.cadena()}"

    def escribe(self):
        print(self.cadena())


