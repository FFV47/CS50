#include <ctype.h>
#include <stdio.h>

int collatz(int n);

int main(int argc, char const *argv[])
{
    int n;
    printf("Digite um numero: \n");
    scanf("%i", &n);
    int steps = collatz(n);
    printf("\nsteps: %i\n", steps);
    return 0;
}

int collatz(int n)
{
    if (n == 1)
    {
        printf("%i", n);
        return 0;
    }
    else if (n % 2 == 0)
    {
        printf("%i -> ", n);
        return 1 + collatz(n / 2);
    }
    else
    {
        printf("%i -> ", n);
        return 1 + collatz(3 * n + 1);
    }
}
