import csv
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return

    database_filename = sys.argv[1]
    sequence_filename = sys.argv[2]

    # Read the database file into memory
    people = []
    with open(database_filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            people.append(row)

    # Read the DNA sequence file into memory
    with open(sequence_filename, "r") as file:
        sequence = file.read()

    # Extract the STRs from the first row of the database file
    str_names = reader.fieldnames[1:]

    # Find the longest match of each STR in the DNA sequence
    str_counts = {str_name: longest_match(sequence, str_name) for str_name in str_names}

    # Check database for matching profiles
    for person in people:
        if all(int(person[str_name]) == str_counts[str_name] for str_name in str_names):
            print(person["name"])
            return

    print("No match")

def longest_match(sequence, subsequence):
    """Returns the longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0

        while sequence[i + count * subsequence_length : i + (count + 1) * subsequence_length] == subsequence:
            count += 1

        longest_run = max(longest_run, count)

    return longest_run

if __name__ == "__main__":
    main()
