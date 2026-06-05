with open("example.txt", 'r') as file:
    x = sum(1 for line in file)

print(x) 