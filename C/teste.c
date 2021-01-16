#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    FILE *fp;
    // char str[60];
    // char *string = NULL;

    /* opening file for reading */
    fp = fopen("dict", "r");
    if (fp == NULL)
    {
        perror("Error opening file");
        return (-1);
    }
    int n = 0;
    char *str = NULL;
    while (1)
    {
        char *string = malloc(20 * sizeof(char));

        str = fgets(string, 20, fp);
        if (str == NULL)
        {
            free(string);
            break;
        }

        if (str[strlen(str) - 1] == '\n')
        {
            str[strlen(str) - 1] = '\0';
        }
        printf("word: %s\n", str);
        printf("%lu\n", strlen(str));
        for (int i = 0, len = strlen(str); i < len; i++)
        {
            printf("%c - %i\n", str[i], i);
        }
        n++;
        free(string);
    }

    printf("\n");
    fclose(fp);

    return (0);
}
