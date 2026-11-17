#include <stdio.h>

int a = 10;
int x;
double media;
double total = 10;
double fixo = 8.25;

double mediaNota(double media) {
    char esqueca[80] = "Cê tá doidoooo kkkkj";
    double resultado;
    
    resultado = fixo + media / 2 + total;
    
    printf("%s\n", esqueca);
    printf("O resultado desta bagaça é: %f\n", resultado);

    return resultado; 
}

int main() {
    x = a + 5;
    media = x - 2;

    mediaNota(media);

    return 0;
}