file = open("data.txt", "r")
x = 0

while True:
    line = file.readline()
    if not line:
        break
    x += 1

print(x)
file.close