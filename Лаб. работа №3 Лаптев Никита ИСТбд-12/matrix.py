def read_matrix(f): return [list(map(int, line.split())) for line in open(f)]
def print_matrix(m, name): print(f"\n{name}:"); [print(" ".join(f"{x:4}" for x in row)) for row in m]
def transpose(m): return [list(row) for row in zip(*m)]
def mul(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(A))) for j in range(len(A))] for i in range(len(A))]
def add(A, B): return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]
def scalar_mult(K, M): return [[K * x for x in row] for row in M]

def get_regions(n):
    r1, r2, r3, r4 = [], [], [], []
    for i in range(n):
        for j in range(n):
            if i < j and i + j < n - 1: r1.append((i, j))
            elif i < j and i + j > n - 1: r2.append((i, j))
            elif i > j and i + j > n - 1: r3.append((i, j))
            elif i > j and i + j < n - 1: r4.append((i, j))
    return r1, r2, r3, r4

def build_F(A):
    n, F = len(A), [row[:] for row in A]
    r1, r2, r3, _ = get_regions(n)
    min_val = min(A[i][j] for i, j in r2)
    min_cnt = sum(1 for i, j in r2 if j % 2 == 1 and A[i][j] == min_val)
    max_val = max(A[i][j] for i, j in r1)
    max_cnt = sum(1 for i, j in r1 if i % 2 == 0 and A[i][j] == max_val)
    print(f"\nМинимумов в нечётных столбцах области 2: {min_cnt}")
    print(f"Максимумов в чётных строках области 1: {max_cnt}")
    swap = zip(r1, r2) if min_cnt > max_cnt else zip(r2, r3)
    for (i1, j1), (i2, j2) in swap: F[i1][j1], F[i2][j2] = F[i2][j2], F[i1][j1]
    return F

def main():
    K = int(input("Введите K: "))
    A = read_matrix("matrix.txt")
    print_matrix(A, "Матрица A")
    F = build_F(A)
    print_matrix(F, "Матрица F")
    result = add(mul(A, A), scalar_mult(K, transpose(A)))
    print_matrix(result, "Результат A*A + K*A^T")

main() # Лаптев Никита ИСТбд-12
