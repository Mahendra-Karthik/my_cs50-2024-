#include <cs50.h>
#include <stdio.h>

// Function prototypes
int get_height(void);
void print_pyramid(int height);

int main(void)
{
    // Get a valid height from the user
    int height = get_height();

    // Print the pyramid of the specified height
    print_pyramid(height);

    return 0;
}

// Function to prompt the user for a valid height
int get_height(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    } while (height < 1);
    return height;
}

// Function to print the pyramid
void print_pyramid(int height)
{
    for (int row = 1; row <= height; row++)
    {
        // Print the spaces
        for (int space = 0; space < height - row; space++)
        {
            printf(" ");
        }

        // Print the hashes
        for (int hash = 0; hash < row; hash++)
        {
            printf("#");
        }

        // Move to the next line
        printf("\n");
    }
}
