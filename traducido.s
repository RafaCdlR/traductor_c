.file	/home/rafa/rcr/UCA/4GII/PL/Practicas/traductor_c/tests/cosasc.c
Section.rodata    
.S0: 
    .text "esto es un print %i"


.S0: 
    .text "esto es un print %i"







################ FUNCION main ####################





.text 

.globl main 

.type main, @function 

main:  

pushl %ebp 

movl %esp, %ebp
subl $8 %esp
abc
#Nodoasignacion

movl $5 -4(%ebp)

#Nodoprint

pushl -8(%ebp)
pushl s0

call printf
addl $8 esp


#Nodoprint

pushl -8(%ebp)
pushl s0

call printf
addl $8 esp


# el return : 

movl $0 $eax
movl %ebp, %esp  
popl %ebp 
ret  
