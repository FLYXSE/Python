import os

for dirpath, dirnames, filenames in os.walk("."):
    for dirname in dirnames:
        print("Каталог: ", os.path.join(dirpath, dirname))
    for filename in filenames:
        print("Файл: ", os.path.join(dirpath, filename))