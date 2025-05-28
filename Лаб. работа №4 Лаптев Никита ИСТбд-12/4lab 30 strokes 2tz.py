import numpy as np
import matplotlib.pyplot as plt

def load_matrix():
    try: return np.loadtxt("matrix_data.txt", dtype=int)
    except: raise FileNotFoundError("Файл matrix_data.txt не найден или повреждён")

def split_blocks(A):
    h = A.shape[0] // 2
    return A[:h, :h], A[:h, h:], A[h:, :h], A[h:, h:]

def build_F(A):
    F = A.copy()
    E, B, _, C = split_blocks(A)
    zero_rows = sum(all(B[i, j] == 0 for j in range(0, B.shape[1], 2)) for i in range(B.shape[0]))
    pos_sum = sum(x for i, row in enumerate(A) if i % 2 == 0 for x in row if x > 0)
    print(f"Нулевых строк в чётных столбцах B: {zero_rows}\nСумма положит. в чётных строках A: {pos_sum}")
    if zero_rows > pos_sum:
        F[:B.shape[0], :B.shape[1]], F[B.shape[0]:, B.shape[1]:] = np.flip(C, axis=0), np.flip(E, axis=0)
    else:
        F[:B.shape[0], :B.shape[1]], F[:B.shape[0], B.shape[1]:] = B.copy(), E.copy()
    return F

def compute_result(A, F, K):
    try:
        if np.linalg.det(A) > np.trace(F):
            return np.linalg.inv(A) @ A.T - K * np.linalg.inv(F)
        return (A.T + np.tril(A) - F.T) * K
    except np.linalg.LinAlgError:
        return "Ошибка: одна из матриц необратима"

def plot_graphs(F):
    plt.figure(figsize=(15, 4))
    for i, (title, data) in enumerate([
        ("Тепловая карта F", F),
        ("Среднее по столбцам", F.mean(axis=0)),
        ("Гистограмма значений F", F.flatten())
    ]):
        plt.subplot(1, 3, i+1)
        plt.imshow(data, cmap='coolwarm') if i == 0 else plt.plot(data, 'o-') if i == 1 else plt.hist(data, bins=10, color='skyblue')
        plt.title(title)
    plt.tight_layout(); plt.show()

def main():
    K = int(input("Введите K: "))
    A = load_matrix()
    print("Матрица A:\n", A)
    F = build_F(A)
    print("Матрица F:\n", F)
    print("Результат:\n", compute_result(A, F, K))
    plot_graphs(F)

if __name__ == "__main__":
    main()
