txt = input("Введите предлодение: ")

words = txt.split()

words_two = set(words)


print(len(words))
print(len(words_two))
print(sorted(words_two))