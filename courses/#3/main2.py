k = int(input("Введите K: "))

p = 1
i = 1

while i <= k:
    p = p * i
    i = i + 1

print(f"Факториал из {k} = {p}")