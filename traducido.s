.file	/home/rafa/rcr/UCA/4GII/PL/Practicas/traductor_c/tests/cosasc.c

.globl x




################ FUNCION prueba ####################





.text 

.globl prueba 

.type prueba, @function 

prueba:  

pushl %ebp 

movl %esp, %ebp
subl $0 %esp

# el return : 


# k _ 1


#    ##k _ 1##   

movl 8(%ebp), %eax
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
#declaracion : a con 1 posiciones
#declaracion : b con 1 posiciones
#declaracion : c con 3000 posiciones
subl $12008 %esp

#tuple


 FALTA NODO : ([
# Asignacion : 


#    ##2##   

movl $2, %eax
movl $eax 0(x)
, 
# Asignacion : 


#    ##5##   

movl $5, %eax
movl $eax 0(%ebp)
, 
# Asignacion : 


#    ##3##   

movl $3, %eax
movl $eax -4(%ebp)
, 
# Asignacion : 


#    ##7##   

movl $7, %eax
movl $eax -5084(%ebp)
, 
# Asignacion : 


#    ##2##   

movl $2, %eax
pushl $eax
call prueba
addl $4 esp

movl $eax -384(%ebp)
], 
#    ##a _ 1##   

movl 0(%ebp), %eax
pushl %eax

#    ##b _ 1##   

movl -4(%ebp), %ebx

#  ##a _ 1+b _ 1## 

popl %eax
addl %ebx, %eax

cmpl $0, %eax
 je if1_fin

# Asignacion : 


#    ##x _ 1##   

movl 0(x), %eax
movl $eax -4(%ebp)

if1_fin:

) 

# el return : 


# 0


#    ##0##   

movl $0, %eax
movl %ebp, %esp  
popl %ebp 
ret  



 ############GLOBALES ##########3: 



{'prueba': funcion : prueba
, 'main': funcion : main
, 'x': x _ 1}