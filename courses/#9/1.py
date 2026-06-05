users = {
        "FLYXSE": "xe9001le",
        "Pasha": "Pasha1234",
        "Sofi": "Stupid"
}

key = input("Введите свой Key: ")

if key in users:
    user = users[key]
    print(f"Имя: {key}\nПароль: {users[key]}")
else:
    print("Пользователь с таким именем не найден!")