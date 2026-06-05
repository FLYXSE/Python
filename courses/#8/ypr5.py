inp = input("Введите числа (через пробел): ")
num = list(map(int, inp.split()))

nathree = tuple(x for x in num if x % 3 == 0)
print(list(nathree))
palindromes = [n for n in num if str(n) == str(n)[::-1]]
print(palindromes)