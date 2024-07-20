#include <cs50.h>
#include <stdio.h>

// Function prototypes
int get_cents(void);
int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    // Prompt the user for change owed, in cents
    int cents = get_cents();

    // Calculate the number of each coin needed
    int quarters = calculate_quarters(cents);
    cents -= quarters * 25;

    int dimes = calculate_dimes(cents);
    cents -= dimes * 10;

    int nickels = calculate_nickels(cents);
    cents -= nickels * 5;

    int pennies = calculate_pennies(cents);
    cents -= pennies * 1;

    // Sum the total number of coins
    int total_coins = quarters + dimes + nickels + pennies;

    // Print the total number of coins
    printf("%d\n", total_coins);

    return 0;
}

// Function to prompt the user for a valid amount of cents
int get_cents(void)
{
    int cents;
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);
    return cents;
}

// Function to calculate the number of quarters needed
int calculate_quarters(int cents)
{
    return cents / 25;
}

// Function to calculate the number of dimes needed
int calculate_dimes(int cents)
{
    return cents / 10;
}

// Function to calculate the number of nickels needed
int calculate_nickels(int cents)
{
    return cents / 5;
}

// Function to calculate the number of pennies needed
int calculate_pennies(int cents)
{
    return cents;
}
