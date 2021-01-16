"""My Library"""


def inputnum(question):
    """input() that only accept numbers characters"""
    answer = input(question)
    while True:
        if answer.isnumeric():
            return answer
        else:
            answer = input(question)


def inputalpha(question):
    """input() that only accept non-numbers characters"""
    answer = input(question)
    while True:
        if answer.isalpha():
            return answer
        else:
            answer = input(question)
