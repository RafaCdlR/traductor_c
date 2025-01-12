int a; // Esto es la declaración de una variable global
int b, c; // Esto son las declaraciones de varias variables globales

void prueba() {
  a = 3;
}

int main() {
  a = 3;
  b = 57;
  c = 100;
  prueba();
  return 0;
}
