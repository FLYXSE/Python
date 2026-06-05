file = open("test.txt", "w")

print("Имя файла: ", file.name)
print(file.mode)
print(file.closed)
file.close()
print(file.closed)