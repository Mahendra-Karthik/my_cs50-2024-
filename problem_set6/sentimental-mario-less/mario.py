def main():
    height = get_height()
    pyramid(height)

def get_height():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                return height
        except ValueError:
            pass

def pyramid(height):
    for i in range(1, height + 1):
        spaces = " " * (height - i)
        hashes = "#" * i
        print(spaces + hashes)

if __name__ == "__main__":
    main()
