import random
a = "Камень"
b = "Ножницы"
c = "Бумага"

abc = ['a', 'b', 'c']



x = 0 #игрок
y = 0 # пк


while True:
 if x == 3 or y == 3:
     if x == 3:
         print("Победил игрок")
         break
     else:
         print("Победил ПК")
         break
 else:
    pc = random.choice(abc)
    print(pc)
    usr = input(f'Выбери - a, b, c: ')
    if pc == usr:
        print("Нечья!")
    elif pc == "а" and usr == "b":
        y += 1
        print("Ты проиграл!")
    elif pc == "a" and usr == "c":
        x += 1
        print("Ты победил!")
    elif pc == "b" and usr == "a":
        x += 1
        print("Ты победил!")
    elif pc == "b" and usr == "c":
        y += 1
        print("Ты проиграл!")
    elif pc == "c" and usr == "a":
        y += 1
        print("Ты проиграл!")
    elif pc == "c" and usr == "b":
        x += 1
        print("Ты победил!")

спасибо
