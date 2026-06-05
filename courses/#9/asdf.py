inp = input("Введите строку: ")
sim = {}

for char in inp:
    if char in sim:
        sim[char] += 1
    else:
        sim[char] = 1 
        
print(sim)