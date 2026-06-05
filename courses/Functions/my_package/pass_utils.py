import random
import string


def generate_password(length):
    if length <= 0:
        raise ValueError("Длина пароля должна быть больше 0")
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password