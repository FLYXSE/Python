a = [1, 2, 3, 4, 5]
k = int(input("На сколько сдвинуть: "))

sdv = a[-k:] + a[:-k]
print(sdv)