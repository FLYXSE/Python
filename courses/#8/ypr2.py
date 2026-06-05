lst = input("ользователь вводит строку: ")
glas = "аеёиоуыэюя"
count = 0

for char in lst:
    if char.lower() in glas:
        count += 1

print(count)