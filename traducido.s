.file	/home/prodrik/Escritorio/pl/traductor_c/tests/cosasc.c

.globl a
.globl b

.text 

.globl main 

.type main, @function 

main:  

pushl %ebp 

movl %esp, %ebp
subl $8 %esp

#NodoIF


# a&&b

movl $a$, %eax
movl $b$, %ebx

#  a&&b 

andl %ebx, %eax

cmpl $0, %eax
 je if1_fin

# ['a'] = a+1

movl $a$, %eax
movl $1$, %ebx

#  a+1 

addl %ebx, %eax

movl $eax$ $a$
jmp else1_fin

if1_fin:


# ['b'] = b+1

movl $b$, %eax
movl $1$, %ebx

#  b+1 

addl %ebx, %eax

movl $eax$ $b$

else1_fin:


# el return : 

movl $0$ $eax$
movl %ebp, %esp  
popl %ebp 
ret  
