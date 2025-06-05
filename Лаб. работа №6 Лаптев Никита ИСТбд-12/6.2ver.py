import math
import timeit
import pandas as pd
import matplotlib.pyplot as plt

# Рекурсия
def F_recursive(n):
    if n == 0:
        return 5.0
    if n == 1:
        return 1.0
    sign = 1 if n % 2 == 0 else -1
    if n % 2 == 0:
        return sign * (2 * F_recursive(n - 1) - F_recursive(n - 2))
    return F_recursive(n - 2) / (math.factorial(2 * n) - F_recursive(n - 1)) #использовали math

# Итерация
def F_iterative(n):
    if n == 0:
        return 5.0
    if n == 1:
        return 1.0
    
    f_prev2 = 5.0  # F(0)
    f_prev1 = 1.0  # F(1)
    factorial = 2  # (2 * 1)! = 2

    for i in range(2, n + 1):
        factorial *= (2 * i) * (2 * i - 1)  # вычисление факториала по предыдущему
        sign = 1 if i % 2 == 0 else -1
        if i % 2 == 0:
            f_current = sign * (2 * f_prev1 - f_prev2)
        else:
            f_current = f_prev2 / (factorial - f_prev1)
        f_prev2, f_prev1 = f_prev1, f_current
    
    return f_prev1

# Сбор данных
results = []
for n in range(0, 21):
    rec_time = timeit.timeit(lambda: F_recursive(n), number=10)
    itr_time = timeit.timeit(lambda: F_iterative(n), number=10)
    rec_val = F_recursive(n)
    itr_val = F_iterative(n)
    results.append((n, rec_val, itr_val, rec_time, itr_time))

# Таблица
df = pd.DataFrame(results, columns=['n', 'Recursive Value', 'Iterative Value', 'Recursive Time (s)', 'Iterative Time (s)'])
print(df)

# График
plt.figure(figsize=(10, 6))
plt.plot(df['n'], df['Recursive Time (s)'], label='Recursive', linestyle='--')
plt.plot(df['n'], df['Iterative Time (s)'], label='Iterative', linestyle='-')
plt.xlabel('n')
plt.ylabel('Time (s)')
plt.legend()
plt.title('Сравнение времени выполнения: рекурсивный и итеративный методы')
plt.grid(True)
plt.show()
