YO = int(input("Сколько вам лет? - "))


if YO<=12:
	print("Вы Ребенок")
elif YO>12 and YO<=17:
	print("Вы Подросток")
elif YO>=18 and YO<65:
	print("Вы Взрослый")
else:
	print("Вы Пенсионер")