file = open("numbers.txt", "r")

numbers = []

for line in file:
    numbers.append(int(line))

file.close()


print("Количество чисел:", len(numbers))
print("Сумма чисел:", sum(numbers))
print("Среднее арифметическое:", round(sum(numbers) / len(numbers), 1))
print("Максимальное число:", max(numbers))
print("Минимальное число:", min(numbers))