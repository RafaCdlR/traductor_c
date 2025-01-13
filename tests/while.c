int main() {
    int i;
    i = 0;

    while (i < 3) {
        int j;
	j = 0;
        while (j < 2) {
            printf("i = %d, j = %d\n", i, j);
            j = j+1;
        }
        i = i+1;
    }

    return 0;
}
