x="\n\n1 — Добавить запись\n2 — Показать все записи\n3 — Найти запись по ключевому слову\n4 — Выйти\n"


while True:
    print(x)
    ans = int(input("Выебирте действие: "))

    if ans == 1:
        with open("diary.txt", "a") as file:
            while True:
                line = input()
                if line == "":
                    break
                file.write(line + "\n")
        file.close

        aq
    if ans == 2:
        with open("diary.txt", "r") as file:
            for line in file:
                print(line.strip())
        file.close()

    
    if ans == 3:
        word = input("Введите слово для поиска: ")
        with open("diary.txt", "r") as file:
        
            found = False
            for line in file:
                if word.lower() in line.lower():
                    print(line.strip())
                    found = True

            if not found:
                print("Ничего не обноруженно!")
        file.close

    
    if ans == 4:
        exit()