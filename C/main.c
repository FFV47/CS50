#include <stdio.h>
#include <string.h>

int main(int argc, char const *argv[])
{
    char *s = "pneumonoultramicroscopicsilicovolcanoconiosis";
    printf("len: %lu\n", strlen(s));
    printf("last: %i\n", s[strlen(s)]);
    return 0;
}
