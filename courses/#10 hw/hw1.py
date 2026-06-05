st = input("Введите строку: ")

file = open("data.txt", "w+")
file.write(st)
file.close