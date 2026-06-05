inp = input("Введите целые числа через пробел: ")
num = tuple(map(int, inp.split()))


is_ascending = all(num[i] < num[i+1] for i in range(len(num)-1))
is_descending = all(num[i] > num[i+1] for i in range(len(num)-1))

print("Кортеж:", num)
if is_ascending:
    print("Вердикт: Строго возрастающий")
elif is_descending:
    print("Вердикт: Строго убывающий")
else:
    print("Вердикт: Не упорядочен")
