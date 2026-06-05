#не моё

password = input("Введите пароль: ")

if len(password) >= 8:
    if "0" in password or "1" in password or "2" in password or "3" in password or "4" in password or "5" in password or "6" in password or "7" in password or "8" in password or "9" in password:
        if "A" in password or "B" in password or "C" in password or "D" in password or "E" in password or "F" in password or "G" in password or "H" in password or "I" in password or "J" in password or "K" in password or "L" in password or "M" in password or "N" in password or "O" in password or "P" in password or "Q" in password or "R" in password or "S" in password or "T" in password or "U" in password or "V" in password or "W" in password or "X" in password or "Y" in password or "Z" in password:
            if "!" in password or "@" in password or "#" in password or "$" in password or "%" in password or "^" in password or "&" in password or "*" in password:
                print("ПАРОЛЬ ПРИНЯТ!")
            else:
                print("ОШИБКА: нет спецсимволов (!@#$%^&*)")
        else:
            print("ОШИБКА: нет заглавных букв")
    else:
        print("ОШИБКА: нет цифр")
else:
    print("ОШИБКА: пароль слишком короткий (нужно минимум 8 символов)")