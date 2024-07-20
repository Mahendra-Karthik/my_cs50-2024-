#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // Check for proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open the memory card file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Buffer to store a block of data
    uint8_t buffer[BLOCK_SIZE];

    // Variables to keep track of the JPEG files
    FILE *img = NULL;
    int file_count = 0;
    char filename[8];
    bool found_jpeg = false;

    // Read the memory card file block by block
    while (fread(buffer, sizeof(uint8_t), BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        // Check if the block indicates the start of a new JPEG file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If a JPEG is already found, close the current file
            if (found_jpeg)
            {
                fclose(img);
            }
            else
            {
                found_jpeg = true;
            }

            // Create a new JPEG file
            sprintf(filename, "%03i.jpg", file_count);
            img = fopen(filename, "w");
            file_count++;
        }

        // If a JPEG file is found, write the block to it
        if (found_jpeg)
        {
            fwrite(buffer, sizeof(uint8_t), BLOCK_SIZE, img);
        }
    }

    // Close any remaining files
    if (img != NULL)
    {
        fclose(img);
    }

    // Close the memory card file
    fclose(file);

    return 0;
}

