import timeit
import pandas as pd
import matplotlib.pyplot as plt

MAX_N = 20

def factorial_iter(k: int) -> int:
    result = 1
    for i in range(2, k + 1):
        result *= i
    return result

def F_recursive(n: int) -> float:
    if n == 0:
        return 5.0
    if n == 1:
        return 1.0

    sign = 1 if n % 2 == 0 else -1

    if n % 2 == 0:
        return sign * (2 * F_recursive(n - 1) - F_recursive(n - 2))
    else:
        return F_recursive(n - 2) / (factorial_iter(2 * n) - F_recursive(n - 1))

def F_iterative(n: int) -> float:
    if n == 0:
        return 5.0
    if n == 1:
        return 1.0
    f_prev2, f_prev1 = 5.0, 1.0
    import math
    for i in range(2, n + 1):
        sign = 1 if i % 2 == 0 else -1
        if i % 2 == 0:
            f_current = sign * (2 * f_prev1 - f_prev2) #ввели
        else:
            f_current = f_prev2 / (math.factorial(2 * i) - f_prev1)
        f_prev2, f_prev1 = f_prev1, f_current
    return f_prev1

if __name__ == "__main__":
    ns = list(range(0, MAX_N + 1))
    results = []
    print(f"{'n':>3} | {'RecVal':>10} | {'ItrVal':>10} | {'RecTime':>10} | {'ItrTime':>10}")
    print('-' * 60)
    for n in ns:
        rec_val = F_recursive(n)
        itr_val = F_iterative(n)
        rec_time = timeit.timeit(lambda: F_recursive(n), number=1000)
        itr_time = timeit.timeit(lambda: F_iterative(n), number=1000)
        results.append((n, rec_val, itr_val, rec_time, itr_time))
        print(f"{n:>3} | {rec_val:>10.4f} | {itr_val:>10.4f} | {rec_time:>10.6f} | {itr_time:>10.6f}")

    df = pd.DataFrame(results, columns=['n', 'Recursive Value', 'Iterative Value', 'Recursive Time (s)', 'Iterative Time (s)'])
    plt.figure(figsize=(8, 5))
    plt.plot(df['n'], df['Recursive Time (s)'], label='Recursive', linestyle='--')
    plt.plot(df['n'], df['Iterative Time (s)'], label='Iterative', linestyle='-')
    plt.xlabel('n')
    plt.ylabel('Time (s)')
    plt.title('Сравнение времени: рекурсивный vs итеративный')
    plt.legend()
    plt.grid(True)
    plt.show()
