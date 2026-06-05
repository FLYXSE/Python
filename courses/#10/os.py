import os

print("Текущая деректория: ", os.getcwd())
os.mkdir("testf")

os.chdir("testf")
print("Текущая деректория: ", os.getcwd())




