# Пользователь вводит строку. Программа подсчитывает, сколько в ней:
# 1 заглавных букв (A–Z, А–Я)
# 2 строчных букв (a–z, а–я)
# 3 цифр
# 4 остальных символов (пробелы, знаки препинания и т.д.)

str = input("Введите строку: ")

isupper = 0
islower = 0
isdigit = 0
other = 0

for symb in str:
    if symb.isupper():
        isupper = isupper + 1
    elif symb.islower():
        islower = islower + 1
    elif symb.isdigit():
        isdigit = isdigit + 1
    else:
        other = other + 1
        
print(f"""
Заглавных: {isupper}
Строчных: {islower}
Цифр: {isdigit}
Других: {other}
""")
