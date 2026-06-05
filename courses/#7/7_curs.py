math = {"Иванов", "Петров", "Сидоров", "Козлов"}
physics = {"Петров", "Смирнов", "Васильев", "Козлов"}
cs = {"Сидоров", "Васильев", "Михайлов", "Никитин"}

one = math | physics | cs
print("Сколько всего уникальных учеников посещают хотя бы один кружок: ", len(one))

two = math & physics & cs
print("Фамилии тех, кто посещает все три кружка: ", two)


only_math_phys = (math & physics) - cs
only_math_cs   = (math & cs) - physics
only_phys_cs   = (physics & cs) - math

three = only_math_phys | only_math_cs | only_phys_cs
print("Фамилии тех, кто посещает ровно два кружка: ", three)

only_math = math - (physics | cs)
only_phys = physics - (math | cs)
only_cs   = cs - (math | physics)

four = only_math | only_phys | only_cs
print("Фамилии тех, кто посещает только один кружок: ", four)