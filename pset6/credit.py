#!/home/fernando/Anaconda/envs/dev/bin/python

import re
import get

card = get.inputnum("Number: ")

soma = 0

for i, num in enumerate(card[::-1]):
    if i % 2 != 0:
        digit = int(num) * 2
        if digit // 10 != 0:
            soma += digit // 10
            soma += digit % 10
        else:
            soma += digit
    else:
        soma += int(num)

if soma % 10 == 0:
    if re.search("^34|37", card) and len(card) == 15:
        print("AMEX")
    elif re.search("^51|52|53|54|55", card) and len(card) == 16:
        print("MASTERCARD")
    elif re.search("^4", card) and len(card) == 13 or len(card) == 16:
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")
