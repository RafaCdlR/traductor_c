int suma(int a, int b) {
    return a + b;
}

// Función que no devuelve nada
void mensaje() {
    printf("Esta función no devuelve ningún valor\n");
}

int f(int a, int b ,int c){
  int d;
  d = 10;
  return a+c+b+d;
}

int f2(int a){
  return a;
}

void f3(){}

int main() {
  int resultado;
  int a,c;
    
  resultado = suma(5, 10);
  printf("Resultado de la suma: %d\n", resultado);

  mensaje();

  a = f(5,1,4);
  c = f2(a);
  //c = f2() invalid wrong number of parameters
  //c = f3() invalid f3 is void
  scanf("insert number %i",&a);
  printf("this is a print : %i",a);

  return 0;
}
