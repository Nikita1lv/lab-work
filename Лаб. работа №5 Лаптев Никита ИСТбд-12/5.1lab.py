import timeit
from itertools import combinations

def algorithmic_method(k1, k2, N):
    sales_team = [f"Продажи_{i}" for i in range(1, k1 + 1)]
    marketing_team = [f"Реклама_{i}" for i in range(1, k2 + 1)]
    all_employees = sales_team + marketing_team
    result = []

    def generate_combinations(current_team, remaining_employees):
        if len(current_team) == N:
            result.append(current_team)
            return
        if not remaining_employees:
            return
        generate_combinations(current_team + [remaining_employees[0]], remaining_employees[1:])
        generate_combinations(current_team, remaining_employees[1:])

    generate_combinations([], all_employees)
    return result[:9]  # Ограничиваем вывод до 9 комбинаций

def python_method(k1, k2, N):
    sales_team = [f"Продажи_{i}" for i in range(1, k1 + 1)]
    marketing_team = [f"Реклама_{i}" for i in range(1, k2 + 1)]
    all_employees = sales_team + marketing_team
    return list(combinations(all_employees, N))[:9]  # Ограничиваем вывод до 9 комбинаций

def optimized_method(k1, k2, N, min_sales):
    sales_team = [f"Продажи_{i}" for i in range(1, k1 + 1)]
    marketing_team = [f"Реклама_{i}" for i in range(1, k2 + 1)]
    all_employees = sales_team + marketing_team
    combinations_list = list(combinations(all_employees, N))[:9]  # Ограничиваем вывод до 9 комбинаций
    return [combo for combo in combinations_list if sum(1 for member in combo if "Продажи" in member) >= min_sales]

k1, k2, N = 3, 2, 3

print("Алгоритмический метод")
algo_result = algorithmic_method(k1, k2, N)
for idx, combo in enumerate(algo_result, 1):
    print(f"{idx}) {', '.join(combo)}")
print(f"\nВсего выведено комбинаций: {len(algo_result)}")

print("\nМетод с itertools")
py_result = python_method(k1, k2, N)
for idx, combo in enumerate(py_result, 1):
    print(f"{idx}) {', '.join(combo)}")
print(f"\nВсего выведено комбинаций: {len(py_result)}")

print("\nСравнение скорости выполнения:")
print(
    "Алгоритмический:",
    timeit.timeit(lambda: algorithmic_method(k1, k2, N), number=100),
    "\nitertools:",
    timeit.timeit(lambda: python_method(k1, k2, N), number=100)
)

min_sales = 2
optimal_combinations = optimized_method(k1, k2, N, min_sales)

print(f"\nОптимизированные варианты (не менее {min_sales} из отдела продаж):")
for idx, combo in enumerate(optimal_combinations, 1):
    print(f"{idx}) {', '.join(combo)}")
print(f"\nВсего выведено подходящих вариантов: {len(optimal_combinations)}")