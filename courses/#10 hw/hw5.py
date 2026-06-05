def main():
    word = input("Введите слово для поиска: ").strip()
    
    if not word:
        print("Ошибка: слово не может быть пустым!")
        return
    
    try:
        with open('data.txt', 'r', encoding='utf-8') as file:
            found = False
            print(f"\nРезультаты поиска слова '{word}':\n")        
            for line_num, line in enumerate(file, 1):
                if word.lower() in line.lower():
                    clean_line = line.rstrip()
                    print(f"{line_num:3d}: {clean_line}")
                    found = True
            if not found:
                print(f"Слово '{word}' не найдено в файле data.txt")
                
    except FileNotFoundError:
        print("Ошибка: файл 'data.txt' не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()