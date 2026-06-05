time = int(input("Который час? - "))

if time>=5 and time<=11:
	print("У вас Утро")
elif time>=12 and time<=16:
	print("У вас День")
elif time>=17 and time<=21:
	print("У вас Вечер")
elif time>=22 and time<=24:
	print("У вас Ночь")
elif time>=0 and time<=4:
	print("У вас Ночь")
else:
	print("Неверное вермя")