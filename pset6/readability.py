text = str(input("Text: "))

letters = 0
words = 0
sentences = 0
for i in text:
    if i.isalpha():
        letters += 1
    elif i in ".!?":
        sentences += 1

words = len(text.split())

L = (letters / words) * 100
S = (sentences / words) * 100

grade_index = 0.0588 * L - 0.296 * S - 15.8

if grade_index > 16:
    print("Grade 16+")
elif grade_index < 1:
    print("Before Grade 1")
else:
    print(f"Grade {round(grade_index)}")
