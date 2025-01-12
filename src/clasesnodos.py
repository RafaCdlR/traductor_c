import re

def bajar_arbo(nod, prof, cadena,contador = 0, der=False):
    aux = "%ebx" if der else "%eax"

    operators = {
    "*": "mull",       # Multiplicación
    "+": "addl",       # Suma
    "-": "subl"       # Resta
   
    }
    #cadena += "\n#  " + str(type(nod)) + " \n\n"

    if(isinstance(nod,(NodoAnd,NodoOr,NodoopUnario))):
        cadena += nod.cadena()
        return False,False

   

    elif (not isinstance(nod, (Nodotermino, Nodocadena))):

        if (not isinstance(nod, NodoopUnario)):
            pila1 , estermino = bajar_arbo(nod.left, prof+1, cadena,contador, False)
        else:
            pila1 = False

        #mirar si a la derecha hay operacion pa meter en la pila 
        if estermino and hasattr(nod, 'right') and not isinstance(nod.right, (Nodotermino, Nodocadena)):

            cadena += "pushl %eax\n"
            pila1 = True




        

        

        pila2,_ = bajar_arbo(nod.right, prof+1, cadena,contador, True)

        cadena += "\n#  " + nod.cadena() + " \n\n"

        
        
        if pila1:  # sacar de la pila si fuera necesario
            cadena += r"popl %eax"+"\n"
        if pila2:
            cadena += r"popl %ebx"+"\n"

        #operadores especiales

        if nod.operador == '/':
            cadena += "cdq \nidivl %ebx  \n\n"

        #operadores de comparación

        elif nod.operador == '==':
            contador += 1
            cadena += f"""cmpl %ebx, %eax   \nmovl $1 %eax  \njne verdadero{contador}   \nmovl $0 %eax  \nverdadero{contador}:\n\n"""
                        
                        
        elif nod.operador == '!=':
            contador += 1
            cadena += f"""cmpl %ebx, %eax   \nmovl $1 %eax  \nje verdadero{contador}   \nmovl $0 %eax  \nverdadero{contador}:\n\n"""

        elif nod.operador == '<=':
            contador += 1
            cadena += f"""cmpl %ebx, %eax   \nmovl $1 %eax  \njg verdadero{contador}   \nmovl $0 %eax  \nverdadero{contador}:\n\n"""

        elif nod.operador == '>=':
            contador += 1
            cadena += f"""cmpl %ebx, %eax   \nmovl $1 %eax  \njl verdadero{contador}   \nmovl $0 %eax  \nverdadero{contador}:\n\n"""

        elif nod.operador == '<':
            contador += 1
            cadena += f"""cmpl %ebx, %eax   \nmovl $1 %eax  \njge verdadero{contador}   \nmovl $0 %eax  \nverdadero{contador}:\n\n"""

        elif nod.operador == '>':
            contador += 1
            cadena += f"""cmpl %ebx, %eax   \nmovl $1 %eax  \njle verdadero{contador}   \nmovl $0 %eax  \nverdadero{contador}:\n\n"""
            
            
        else:
            cadena += f"{operators[nod.operador]} %ebx, %eax\n\n"

        if prof != 0:
           cadena += "pushl %eax\n"

        
        return True , False

    else:
        cadena += "\n#  " + nod.cadena() + " \n\n"
        cadena += f"movl ${nod.cadena()}$, {aux}\n"
        return False , True #por si hay parentesis a la derecha hay q meter en pila 


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
    def __init__(self, operacion,contador):

        self.esoperacion = True

        if operacion == "":
            cadena = ""

        else:
            cadena = []
            cadena += "\n# " + operacion.cadena()+"\n\n"
            # self.bajar_arbo2(p.operacion,0,cadena)
            # print("\n\n-----\n\n")
            # si no es un id recorre arbol
            if not isinstance(operacion, Nodotermino):
                bajar_arbo(operacion, 0, cadena,contador)

                cadena = "".join(cadena)

            else:
                self.esoperacion = False
                cadena = operacion.cadena()

        self.cad = cadena

    def cadena(self):
        cad = ""

        # si la cadena esta vacia es un void y solo se hace la parte final
        
        if not self.esoperacion and self.cad != "":
            cad = f"movl ${self.cad}$ $eax$\n"
        else:
            cad += self.cad
                

        return cad + "movl %ebp, %esp  \npopl %ebp \nret  \n"


class nodofuncion(Nodo):

    # pushear ebp(base antes de la funcion)
    # luego copiar esp a ebp
    # al final volver a copiar la primera posicion de
    # la base de la pila a ebp (base anterior) (ret)

    def __init__(self, tipo, nombre, parametros, cuerpo, contador,retorno=nodoreturn("",0)):
        print("CUERPO",cuerpo)
        pila = dict()
        self.tipo = tipo
        self.nombre = nombre
        self.parametros = parametros
        self.cuerpo = cuerpo
        self.Variables_texto = []
        self.contador = contador
        self.ensamblador = f"\n\n\n\n################ FUNCION {nombre} ####################\n\n\n\n\n"

        self.ensamblador += f'''
.text \n
.globl {nombre} \n
.type {nombre}, @function \n
{nombre}:  \n
pushl %ebp \n
movl %esp, %ebp\n'''

        contador = 8
        print("funcion : ", nombre, "\n\n")
        for var in parametros:
            print(var)

            if var[1] in pila:  # MANEJO DE ERRORES

                raise ValueError(f"Error: variable repetida {var[1]} en la función {nombre}")

            pila[var[1]] = contador

            contador += 4

        # restar la memoria de los parametros:
        self.ensamblador += f"subl ${contador} %esp\n"
        contador = -4
        # declaraciones
        '''
        for dec in self.cuerpo[0]:
            print(dec)
            if isinstance(dec, Nododeclaracion):
                self.ensamblador += dec.cadena()

                tam = 1
                #sumar las dimensiones para el tamaño del array
                for n in dec.array:
                    tam *= n

                pila[dec.nombre] = f"{contador}(%ebp)"
                contador -= 4*tam
            else:
                self.ensamblador += f"\n FALTA NODO : {dec} \n"
        '''

        if self.cuerpo and self.cuerpo[0]:
            # compruebo si se puede iterar sobre el objeto
            if isinstance(self.cuerpo[0], list):
                for dec in self.cuerpo[0]:
                    print(dec)
                    if isinstance(dec, Nododeclaracion):
                        self.ensamblador += dec.cadena()

                        tam = 1
                        # sumar las dimensiones para el tamaño del array
                        for n in dec.array:
                            tam *= n

                        pila[dec.nombre] = contador
                        contador -= 4 * tam
                    else:
                        self.ensamblador += f"\n FALTA NODO : {dec} \n"
            else:
                dec = self.cuerpo[0]
                print(dec)
                if isinstance(dec, Nododeclaracion):
                    self.ensamblador += dec.cadena()

                    tam = 1
                    # sumar las dimensiones para el tamaño del array
                    for n in dec.array:
                        tam *= n

                    pila[dec.nombre] = contador
                    contador -= 4 * tam
                else:
                    self.ensamblador += f"\n FALTA NODO : {dec} \n"

        print(pila)


        self.simbolos = pila

        if self.cuerpo and self.cuerpo[1]:
            # Instrucciones
            if isinstance(self.cuerpo[1], list):
                for ins in self.cuerpo[1]:
                    
                    if isinstance(ins, Nodo):
                        self.ensamblador += "\n#" + type(ins).__name__ + "\n\n"
                        self.ensamblador += ins.cadena()

                        if isinstance(ins,Nodoprint):#anadir texto a las globales
                            print("DENTRO")
                            print(ins.rodata())
                            self.Variables_texto.append(ins.rodata())

                    else:
                        self.ensamblador += f"\n FALTA NODO : {ins} \n"
            else:
                ins = self.cuerpo[1]
                self.ensamblador += "\n#" + type(ins).__name__ + "\n\n"
                if isinstance(ins, Nodo):
                    self.ensamblador += ins.cadena()

                    if isinstance(ins,Nodoprint):#anadir texto a las globales
                        print("DENTRO")
                        self.Variables_texto.append(ins.rodata())

                else:
                    self.ensamblador += f"\n FALTA NODO : {ins} \n"


        self.ensamblador += "\n# el return : \n\n"  # comentario del return

        # final el return
        
        self.ensamblador += retorno.cadena()

        print("\n\nfin funcion", nombre)

    def cadena(self):
        return f"funcion : {self.nombre}\n"

    def cadena2(self,asm = "",SIMBOLOS_GLOBALES = dict()):
        if len(self.Variables_texto)>0:
            print("CADENA")
            
            asm.append("Section.rodata    \n")
            for text in self.Variables_texto:
                self.contador += 1
                asm.append(f"{text}\n\n") 

           

            
        return self.cambiar_variables(self.ensamblador,SIMBOLOS_GLOBALES)

    def escribe(self):
        print(self.cadena())


    def cambiar_variables(self,texto,simbolos):


        def transformar(texto):
            partes = texto.group(1).split(' ')
            numero  = 0
            #buscar en la tabla
            if partes[0] == "eax" or partes[0] == "ebx":
                texto_encontrado = f"${partes[0]}"
            elif partes[0].isdigit():
                texto_encontrado = f"${int(partes[0])}"
            elif partes[0] in self.simbolos:
                numero = self.simbolos[partes[0]]
                texto_encontrado = f"{numero}(%ebp)" # Captura el texto entre $
                
            elif partes[0] in simbolos:
                numero = simbolos[partes[0]]
                texto_encontrado = f"{numero}" # Captura el texto entre $
            else:
                raise(ValueError(f"LA VARIABLE %{partes[0]}% en la funcion {self.nombre} NO ESTA DEFINIDA : \n tabla global : \n {simbolos} \n\n#############\n\n tabla de funcion : \n {self.simbolos}"))
            

            
            return texto_encontrado 



        return re.sub(r'\$([^\n]+?)\$', transformar, texto)
        
        

'''
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
'''


class Nodotermino(Nodo):
    valor = None  # valor numerico

    def __init__(self, v, simbolo=None, offset=None):
        
        self.nombre = v
        self.simbolo = simbolo
        self.offset = offset

       
    def cadena(self):
        cadena = []
        cadena += self.nombre
        
        if self.simbolo:
            cadena += " "
            cadena += str(self.simbolo)
            

        

        if self.offset:
            cadena += " "
            if isinstance(self.offset,list):
                cadena += ",".join(self.offset)
            else:
                cadena += str(self.offset)
            

        return "".join(cadena)


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

    def __init__(self, operador, right,contador):
        contador += 1
        self.operador = operador
        self.right = right
        cadena = []

        if operador == "!":
                
            cadena += "\n   #NOT\n\n"

            bajar_arbo(right, 0, cadena,contador)

            


            cadena += f"cmpl $0, %eax \nje finalNOT{contador}   \nmovl $0, %eax \nfinalNOT{contador}:\n\n"

            
        else: # posible error
            bajar_arbo(right, 0, cadena,contador)
            cadena += "subl $0 %eax\n"
    
        self.cad = "".join(cadena)



    def cadena(self):
        return self.cad

    def escribe(self):
        print(self.cadena())

'''
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

'''
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

    def __init__(self, nombre, tipo, espuntero=False, array=[1]):
        self.nombre = nombre
        self.tipo = tipo
        self.espuntero = espuntero
        self.array = array

    def cadena2(self):
        p = ""
        if self.espuntero:
            p = "* "

        return f"{self.tipo}{p} {self.nombre} {self.array}"
    
    def cadena(self):
        p = ""
        if self.espuntero:
            p = "* "

        return f"{self.nombre}"

    def escribe(self):
        print(self.cadena())


class Nodoasignacion(Nodo):
    # dest = origen;
    def __init__(self, operacion, dest,contador):  # quito un , sin nada despues de dest
        self.dest = dest

        esoperacion = True
        cadena = []
        
        cadena += "\n# " +str(dest) + " = " + operacion.cadena() + "\n\n"
        # self.bajar_arbo2(p.operacion,0,cadena)
        # print("\n\n-----\n\n")
        # si no es un id recorre arbol
        if not isinstance(operacion, Nodotermino):
            bajar_arbo(operacion, 0, cadena,contador)

            cadena = "".join(cadena)

        else:
            esoperacion = False
            cadena = operacion.cadena()

        self.orig = cadena
        self.esoperacion = esoperacion

    def cadena(self):
        if isinstance(self.dest,list):
            if self.esoperacion:
                cad = self.orig + f"movl $eax$ ${self.dest[-1]}$\n"
            else:
                cad = f"movl ${self.orig}$ ${self.dest[-1]}$\n"

            ant = self.dest[-1]
            for id in self.dest[-2::-1]:
                cad += f"movl ${ant}$ ${id}$\n"
                ant = id
        else:
            if self.esoperacion:
                cad = self.orig + f"movl $eax$ ${self.dest}$\n"
            else:
                cad = f"movl ${self.orig}$ ${self.dest}$\n"



        return cad

    def escribe(self):
        print(self.cadena())


class Nodocadena(Nodo):
    def __init__(self, nombre):
        self.nombre = nombre

    def cadena(self):
        return self.nombre


class NodoWhile(Nodo):
    def __init__(self, operacion, cuerpo , contador):  # quito un , sin nada despues de dest
        self.cuerpo = cuerpo
        self.operacion = operacion
        contador+=1
        self.contador = contador


    
        cadena = []
        cadena += f"while{contador}_ini:"#etiqueta inicio
        cadena += "\n# " + operacion.cadena() + "\n\n"
        # self.bajar_arbo2(p.operacion,0,cadena)
        # print("\n\n-----\n\n")
        # si no es un id recorre arbol
        if not isinstance(operacion, Nodotermino):
            bajar_arbo(operacion, 0, cadena,contador)

            cadena = "".join(cadena)

        else:
            
            cadena += operacion.cadena()

        cadena += f"cmpl $0, %eax\n jne while{contador}_fin\n"
        
        #añadir codigo del cuerpo del bucle while
        
        for ins in cuerpo:
            cadena += ins.cadena()

        #salto final
        cadena += f"jmp while{contador}_ini\n\n while{contador}_fin:\n"

        self.cad = "".join(cadena)
        print(self.cad)
        

    def cadena(self):

        return self.cad

    def escribe(self):
        print(self.cadena())




class NodoIF(Nodo):
    def __init__(self, operacion, cuerpo , else_ , contador):  # quito un , sin nada despues de dest
        self.cuerpo = cuerpo
        self.operacion = operacion
        contador+=1
        self.contador = contador

        hayelse = False
        if else_:
            hayelse = True

    
        cadena = []

        
       

       #CONDICION

        if not isinstance(operacion, Nodotermino):
            bajar_arbo(operacion, 0, cadena,contador)

            cadena = "".join(cadena)

        else:
            
            cadena += operacion.cadena()

        cadena += f"cmpl $0, %eax\n je if{contador}_fin\n"
        
        #CUERPO IF
        
        for ins in cuerpo:
            cadena += ins.cadena()

        #salto final
        if hayelse:
            cadena += f"jmp else{contador}_fin\n"

        cadena += f"\nif{contador}_fin:\n\n"

        #BUCLE ELSE
        if hayelse:

            for ins in else_:
                cadena += ins.cadena()

            cadena += f"\nelse{contador}_fin:\n\n"



        self.cad = "".join(cadena)
        print(self.cad)
        

    def cadena(self):

        return self.cad

    def escribe(self):
        print(self.cadena())



class NodoAnd(Nodo):
    def __init__(self, left , right,contador,operador = ""):  # quito un , sin nada despues de dest
        self.left = left
        self.right = right
        self.operador = operador
        contador += 1

        
        cadena = []
            
       
        
        
        bajar_arbo(left, 0, cadena,contador)

        


        cadena += f"cmpl $0, %eax \nje finalAND{contador}\n"

        

        
       
        bajar_arbo(right, 0, cadena,contador)

            

        
            
        
        
       
        
        cadena += f"finalAND{contador}:\n"

        
        self.cad = "".join(cadena)
        print(self.cad)
        

    def cadena(self):

        return self.cad

    def escribe(self):
        print(self.cadena())





class NodoOr(Nodo):
    def __init__(self, left , right,contador,operador = ""):  # quito un , sin nada despues de dest
        self.left = left
        self.right = right
        self.operador = operador
        contador += 1

        
        cadena = []
            
       
        
        
        bajar_arbo(left, 0, cadena,contador)

        


        cadena += f"cmpl $0, %eax \njne finalOR{contador}\n"

        

        
       
        bajar_arbo(right, 0, cadena,contador)

            

        
            
        
        
       
        
        cadena += f"finalOR{contador}:\n"

        
        self.cad = "".join(cadena)
        print(self.cad)

    def cadena(self):

        return self.cad

    def escribe(self):
        print(self.cadena())




class Nodoprint(Nodo):

    def __init__(self,parametros,contador_variable = 0):
        contador_variable += 0
        cadena = []
        contador = 4
        
        if isinstance(parametros,tuple):
            self.texto = f".S{contador_variable}: \n    .text {parametros[0]}\n"
            
            if isinstance(parametros[1],list):
                for v in parametros[1][::-1]:

                    if isinstance(v,Nododeclaracion):
                        cadena += f"pushl ${v.cadena()}$\n"
                        
                    else:
                        cadena_arbo = []
                        bajar_arbo(v,0,cadena_arbo,contador_variable)
                        cadena += cadena_arbo
                        cadena += f"pushl $eax$\n"
                    contador += 4

            else:
                v = parametros[1]
                if isinstance(v,Nododeclaracion):
                    cadena += f"pushl ${v.cadena()}$\n"
                    
                        
                else:
                    cadena_arbo = []
                    bajar_arbo(v,0,cadena_arbo,contador_variable)
                    cadena += cadena_arbo
                    cadena += f"pushl $eax$\n"
                contador += 4
            cadena += f"pushl s{contador_variable}\n\n"
            cadena += "call printf\n"
            cadena += f"addl ${contador} esp\n\n"
        else:
            self.texto = f".S{contador_variable}: \n    .text {parametros}\n"

        self.cad = "".join(cadena)

    def cadena(self):

        return self.cad
    
    def rodata(self):
        print("RODATA",self.texto)
        return self.texto

    def escribe(self):
        print(self.cadena())




class Nodollamada_funcion(Nodo):

    def __init__(self,nombre,parametros,contador_variable = 0):
        contador_variable += 0
        cadena = []
        contador = 0
        
        if parametros:
            
            if isinstance(parametros,list):
                for v in parametros[::-1]:

                    if isinstance(v,Nododeclaracion):
                        cadena += f"pushl ${v.cadena()}$\n"
                        
                    else:
                        cadena_arbo = []
                        bajar_arbo(v,0,cadena_arbo,contador_variable)
                        cadena += cadena_arbo
                        cadena += f"pushl $eax$\n"

                    contador += 4

            else:
                v = parametros
                if isinstance(v,Nododeclaracion):
                    cadena += f"pushl ${v.cadena()}$\n"
                        
                else:
                    cadena_arbo = []
                    bajar_arbo(v,0,cadena_arbo,contador_variable)
                    cadena += cadena_arbo
                    cadena += f"pushl $eax$\n"
                
                contador += 4

            
        cadena += f"call {nombre}\n"
        cadena += f"addl ${contador} esp\n\n"
    
        self.cad = "".join(cadena)

    def cadena(self):

        return self.cad
    
  

    def escribe(self):
        print(self.cadena())



