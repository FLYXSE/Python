inp = input("Введите последовательность целых чисел (через пробел): ")

num = list(map(int, inp.split()))

numt = tuple(num)
print(numt)

numch = tuple(x for x in numt if x % 2 == 0)
numnoch = tuple(x for x in numt if x % 2 != 0)
print(numch)
print(numnoch)