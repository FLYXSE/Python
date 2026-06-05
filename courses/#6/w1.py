a = [0]*5

for i in range(5):
    print("a[", i, "]= ", end = "")
    a[i] = int(input())
    
print(sum(a))