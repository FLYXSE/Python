otlichniki = []
doljniki = []
count = 0

file = open("students.txt", "r")

for line in file:
        name, mark = line.split(":")
        name = name.strip()
        mark = int(mark.strip())
        
        count += 1
        
        if mark == 5:
            otlichniki.append(name)
        if mark == 2:
            doljniki.append(name)
            
file.close

print(f"Отличники: {otlichniki}")
print(f"Должники: {doljniki}")
print(f"Всего студентов: {count}")
