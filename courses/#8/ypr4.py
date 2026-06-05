w1 = input("Первое слово: ")
w2 = input("Второе слово: ")

def proverka(w1, w2):
    s1 = sorted(w1.lower())
    s2 = sorted(w2.lower())
    
    is_anagramma = s1 == s2
    
    return (w1, w2 , is_anagramma)

print(proverka(w1, w2))