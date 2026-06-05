i = 1

while i <= 10:
    print("Цыкл while: ", i, 2**i)
    i=i+1
print("\n")

for i in range(1, 11):
    print("Цыкл for: ", i, 2**i)
print("\n")

x = 1
while True:
    print("Цыкл True: ", x , 2**x)
    x = x + 1
    if x>10:
        break
