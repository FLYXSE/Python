import math
x = int(input("введи x для решения: "))
y = ((5*x + math.sin(x**2) / (2*x + math.tan(x))) + math.fabs(math.sin(x**2)))

print(y)