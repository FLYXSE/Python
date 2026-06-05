# Ввести символ → вывести его код, следующий и предыдущий символ.

str = input("Введите символ: ")
strord = ord(str)
print(chr(strord-1), str, chr(strord+1))