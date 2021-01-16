#include <stdio.h>

int main(int argc, char const *argv[])
{
    int a = 0x01; // 0000 0001
    printf("a = %i\n", a);
    printf("bitwise a << 3: %03i\n", a << 3); // 0000 1000
    printf("bitwise a << 7: %i\n", a << 7);   // 1000 0000

    int b = 0xC0; // 1100 0000
    printf("b = %i\n", b);
    printf("bitwise b >> 4: %i\n", b >> 4); // 0000 1100
    printf("bitwise b >> 6: %i\n", b >> 6); // 0000 0011

    int c = 1;
    printf("int << 31: %i\n", c << 31);
    unsigned int d = 1;
    printf("unsigned int << 31: %i\n", d << 31);

    return 0;
}
