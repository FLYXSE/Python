with open("notes.txt", "w") as file:
    while True:
        line = input()
        if line == "":
            break
        file.write(line + "\n")