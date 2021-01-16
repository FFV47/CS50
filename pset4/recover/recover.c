#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover filename\n");
        return 1;
    }

    // creates pointer to input file
    FILE *sdcard = fopen(argv[1], "r");

    // checks if has enough memory to open file
    if (sdcard == NULL)
    {
        printf("Could not open '%s'\n", argv[1]);
        return 1;
    }

    // creates a buffer to store a block of 512 Bytes, defaults of FAT filesystem
    BYTE *buffer = malloc(512);
    int file_count = 0;
    char filename[8];
    int byte_count;

    do
    {
        if (file_count == 0)
        {
            sprintf(filename, "%03i.jpg", file_count);
            byte_count = fread(buffer, 1, 512, sdcard);
        }
        else
        {
            sprintf(filename, "%03i.jpg", file_count);
        }

        // looks for JPEG header bytes in the first bytes of a block
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // creates a new file and write the first block that belongs to JPEG file
            FILE *jpg = fopen(filename, "w");
            fwrite(buffer, 1, 512, jpg);
            byte_count = fread(buffer, 1, 512, sdcard);

            // keeps writing blocks to a file until all first 4 bytes matches a JPEG header
            while ((buffer[0] != 0xff || buffer[1] != 0xd8 || buffer[2] != 0xff || (buffer[3] & 0xf0) != 0xe0) && byte_count == 512)
            {
                fwrite(buffer, 1, 512, jpg);
                byte_count = fread(buffer, 1, 512, sdcard);
            }
            // if while block is false, it's because a new JPEG file was found or it reached EOF (byte_count != 512)
            fclose(jpg);
            file_count++;
        }
    } // keep the program running until EOF (byte_count would be 0)
    while (byte_count == 512);

    // frees the memory allocated to the buffer
    free(buffer);

    free(sdcard);

    return 0;
}
