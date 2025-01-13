.file	/home/prodrik/Escritorio/pl/traductor_c/tests/funciones.c
.Section_rodata

.S1:     .text "Esta función no devuelve ningún valor\n"
.S2:     .text "Resultado de la suma: %d\n"
.S3:     .text "insert number %i"
.S4:     .text "this is a print : %i"

.end_rodata

################ FUNCION suma ####################





.text 

.globl suma 

.type suma, @function 

suma:  

pushl %ebp 

movl %esp, %ebp
subl $4 %esp

# el return : 


# a _ -1+b _ -1


#    ##a _ -1##   

movl 8(%ebp), %eax
pushl %eax

#    ##b _ -1##   

movl 12(%ebp), %ebx

#  ##a _ -1+b _ -1## 

popl %eax
addl %ebx, %eax

movl %ebp, %esp  
popl %ebp 
ret  





################ FUNCION mensaje ####################





.text 

.globl mensaje 

.type mensaje, @function 

mensaje:  

pushl %ebp 

movl %esp, %ebp
subl $4 %esp

#Nodoprint


pushl s1

call printf
addl $4 esp


# el return : 

movl %ebp, %esp  
popl %ebp 
ret  





################ FUNCION f ####################





.text 

.globl f 

.type f, @function 

f:  

pushl %ebp 

movl %esp, %ebp
#declaracion : d con 1 posiciones
subl $8 %esp

#Nodoasignacion


# Asignacion : 


#    ##10##   

movl $10, %eax
movl $eax -4(%ebp)

# el return : 


# a _ -1+c _ -1+b _ -1+d _ -1


#    ##a _ -1##   

movl 8(%ebp), %eax
pushl %eax

#    ##c _ -1##   

movl 16(%ebp), %ebx

#  ##a _ -1+c _ -1## 

popl %eax
addl %ebx, %eax

pushl %eax

#    ##b _ -1##   

movl 12(%ebp), %ebx

#  ##a _ -1+c _ -1+b _ -1## 

popl %eax
addl %ebx, %eax

pushl %eax

#    ##d _ -1##   

movl -4(%ebp), %ebx

#  ##a _ -1+c _ -1+b _ -1+d _ -1## 

popl %eax
addl %ebx, %eax

movl %ebp, %esp  
popl %ebp 
ret  





################ FUNCION f2 ####################





.text 

.globl f2 

.type f2, @function 

f2:  

pushl %ebp 

movl %esp, %ebp
subl $4 %esp

# el return : 


# a _ -1


#    ##a _ -1##   

movl 8(%ebp), %eax
movl %ebp, %esp  
popl %ebp 
ret  





################ FUNCION f3 ####################





.text 

.globl f3 

.type f3, @function 

f3:  

pushl %ebp 

movl %esp, %ebp
subl $4 %esp

# el return : 

movl %ebp, %esp  
popl %ebp 
ret  





################ FUNCION main ####################





.text 

.globl main 

.type main, @function 

main:  

pushl %ebp 

movl %esp, %ebp
#declaracion : resultado con 1 posiciones
#declaracion : a con 1 posiciones
#declaracion : c con 1 posiciones
subl $16 %esp

#Nodoasignacion


# Asignacion : 


#    ##10##   

movl $10, %eax
pushl $eax

#    ##5##   

movl $5, %eax
pushl $eax
call suma
addl $8 esp

movl $eax -4(%ebp)

#Nodoprint


pushl -4(%ebp)
pushl s2

call printf
addl $8 esp


#Nodollamada_funcion

call mensaje
addl $0 esp


#Nodoasignacion


# Asignacion : 


#    ##4##   

movl $4, %eax
pushl $eax

#    ##1##   

movl $1, %eax
pushl $eax

#    ##5##   

movl $5, %eax
pushl $eax
call f
addl $12 esp

movl $eax -8(%ebp)

#Nodoasignacion


# Asignacion : 

pushl -8(%ebp)
call f2
addl $4 esp

movl $eax -12(%ebp)

#Nodoscanf



#    ##a & -1##   

movl -8(%ebp), %eax
pushl $eax
pushl s3

call scanf
addl $8 esp


#Nodoprint


pushl -8(%ebp)
pushl s4

call printf
addl $8 esp


# el return : 


# 0


#    ##0##   

movl $0, %eax
movl %ebp, %esp  
popl %ebp 
ret  



 ############GLOBALES ##########3: 



{'suma': funcion : suma
, 'mensaje': funcion : mensaje
, 'f': funcion : f
, 'f2': funcion : f2
, 'f3': funcion : f3
, 'main': funcion : main
}