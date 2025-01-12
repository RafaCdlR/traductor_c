

int prueba(int prob) {
  
  return prob *(25+1);
}

int main() {
  int a; // Esto es la declaración de una variable global
  int b, c; // Esto son las declaraciones de varias variables globales
  b = c = a;
 
  prueba(a);
  return 0;
}
