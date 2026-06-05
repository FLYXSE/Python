students = {
    'Анна': {'age': 20, 'grade': 4},
    'Иван': {'age': 19, 'grade': 3}
}
best_name = None
best_info = None
max_grade = 0

for name, info in students.items():
    grade = info["grade"]
    
    if grade > max_grade:
        max_grade = grade
        best_name = name
        best_info = info
        
print(f"Имя: {best_name}\nИнфо: {best_info}")