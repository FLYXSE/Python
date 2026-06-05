file = open("multiplication_table.txt", "w")

for a in range(1, 11):
    for b in range(1, 11):
        line = f"{a} x {b} = {a * b}\n"
        file.write(line)
        
file.close