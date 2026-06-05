dicts = [
    {'a': 1, 'b': 2},
    {'b': 3, 'c': 4},
    {'a': 5, 'c': 1}
]

result = {}

for d in dicts:
    for key, value in d.items():
        if key in result:
            result[key] += value
        else:
            result[key] = value

print(result)