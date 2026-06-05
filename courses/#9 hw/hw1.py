scores = {'Анна': 85, 'Иван': 60, 'Мария': 90}
scores_t = {}

for key, value in scores.items():
    if value >= 80:
        scores_t[key] = value
        
print(scores_t)