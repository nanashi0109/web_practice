import random


def get_random_password(length):
    result = ""
    for i in range(0, length, 1):
        result += get_random_char()
    return result


def get_random_char():
    id_char = random.randint(33, 122)
    return chr(id_char)
