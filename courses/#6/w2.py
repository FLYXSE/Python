a = [0]*7

for i in range(7):
    print("a[", i, "]= ", end = "")
    a[i] = int(input())

min = min(a)
max = max(a)
inmin = a.index(min)
inmax = a.index(max)
    
print(min, inmin)
print(max, inmax)