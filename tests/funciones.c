// Función que devuelve un entero
int suma(int a, int b) {
    return a + b;
}

// Función que no devuelve nada
void mensaje() {
    printf("Esta función no devuelve ningún valor\n");
}

int main() {
    int resultado;
    resultado = suma(5, 10);
    printf("Resultado de la suma: %d\n", resultado);

    mensaje();

    return 0;
}
