import random

x = random.randint(1, 100)
print(x)
print("Компьютер загадал число от 1 до 100. Попробуй угадать!")

att = 0


while True:
    usr = int(input("Введи своё число: "))
    att += 1
    if usr == x:
        print(f"Ты угадал! Число попыток {att}")
        break
    elif usr > x:
        print("Неверно. Число компьютера МЕНЬШЕ.")
    else:
        print("Неверно. Число компьютера БОЛЬШЕ.")

