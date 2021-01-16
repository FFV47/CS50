#!/home/fernando/Anaconda/envs/dev/bin/python

import csv
from sys import argv, exit


def repeatCount(sequence, tandem):
    count = 0
    long = 0
    size = len(tandem)
    i = sequence.find(tandem)

    # if no STR can be found in the sequence
    if i == -1:
        return 0
    while i != -1:
        # count how many consecutive STRs
        while sequence[i : i + size] == sequence[i + size : i + 2 * size]:
            count += 1
            i += size

        # The final STR is not added in the loop
        count += 1
        i += size

        if count >= long:
            long = count

        # find the next sequence
        i = sequence.find(tandem, i)
        count = 0

        # if no more sequence is found return the longer one
        if i == -1:
            return long
    else:
        return long


if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python dna.py [DATABASE] [DNA SEQUENCE]")
        exit(1)

    # CSV files must be opened with kwarg newline='', to work with csv module
    with open(argv[1], newline="") as csvfile:
        with open(argv[2]) as inputSequence:
            database = csv.DictReader(csvfile)
            sequence = inputSequence.read()
            shortTandemRepeats = database.fieldnames[1:]

            # extract profile based on the provided STRs in the database
            profile = {}
            for tandem in shortTandemRepeats:
                profile[tandem] = str(repeatCount(sequence, tandem))

            for userdata in database:
                for key in userdata:
                    if key == "name":
                        continue
                    elif profile[key] != userdata[key]:
                        break
                else:
                    print(userdata["name"])
                    break
            else:
                print("No match")
