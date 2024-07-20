def main():
    change = get_positive_float("Change owed: ")
    coins = calculate_coins(change)
    print(coins)

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
        except ValueError:
            pass

def calculate_coins(change):
    cents = round(change * 100)
    coins = 0

    for coin in [25, 10, 5, 1]:
        coins += cents // coin
        cents %= coin

    return coins

if __name__ == "__main__":
    main()
