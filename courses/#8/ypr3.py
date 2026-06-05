inp1 = input("Первый список: ")
lst1 = list(map(int, inp1.split()))

inp2 = input("Второй список: ")
lst2 = list(map(int, inp2.split()))

pr = set(lst1).symmetric_difference(set(lst2))

print(tuple(sorted(pr)))