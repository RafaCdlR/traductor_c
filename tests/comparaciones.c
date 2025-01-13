int main() {
    int a, b;

    a = 5;
    b = 10;

    if (a == b) {
        printf("a es igual a b\n");
    } else {
      if (a != b && a <= b) {
        printf("a es diferente de b y es menor que b\n");
      }
    }

    if (b >= 10 || a >= 80) {
        printf("Una de las condiciones es verdadera\n");
    }

    return 0;
}
