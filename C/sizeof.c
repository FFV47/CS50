#include <stdio.h>
#include <string.h>

typedef struct node
{
    char word[46];
    struct node *next;
} node;

int main(int argc, char const *argv[])
{
    int *ptr = NULL;
    char arr[20] = {0};
    char arr2[] = {0};

    printf("char: %lu\n", sizeof(char));
    printf("int: %lu\n", sizeof(int));
    printf("long: %lu\n", sizeof(long));
    printf("long long: %lu\n", sizeof(long long));
    printf("float: %lu\n", sizeof(float));
    printf("double: %lu\n", sizeof(double));
    printf("array[20]: %lu\n", sizeof(arr));
    printf("array with 0: %lu\n", sizeof(arr2));
    printf("pointer: %lu\n", sizeof(ptr));
    printf("node: %lu\n", sizeof(node));
    return 0;
}
