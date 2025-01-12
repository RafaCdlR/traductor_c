int a; // Esto es la declaración de una variable global
int b, c; // Esto son las declaraciones de varias variables globales

int prueba(int prob) {
  
  return prob *(25+1);
}

int main() {
  a = 3;
 
  prueba(a);
  return 0;
}
