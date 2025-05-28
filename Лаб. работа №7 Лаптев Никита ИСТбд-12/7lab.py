import tkinter as tk
from tkinter import scrolledtext
from itertools import combinations

def generate_combinations():
    try:
        k1 = int(entry_k1.get())
        k2 = int(entry_k2.get())
        N = int(entry_N.get())
        min_sales = int(entry_min_sales.get())
    except ValueError:
        result_window.insert(tk.END, "Ошибка ввода данных. Проверьте значения.")
        return

    result_window.delete('1.0', tk.END)
    
    # Формируем список сотрудников
    sales_team = [f"Продажи_{i}" for i in range(1, k1 + 1)]
    marketing_team = [f"Реклама_{i}" for i in range(1, k2 + 1)]
    all_employees = sales_team + marketing_team
    
    # Генерируем комбинации
    combinations_list = list(combinations(all_employees, N))
    optimal_combinations = [c for c in combinations_list if sum(1 for member in c if "Продажи" in member) >= min_sales]

    # Выводим результат
    result_window.insert(tk.END, f"Всего комбинаций: {len(optimal_combinations)}\n ")
    for i, combo in enumerate(optimal_combinations, 1):
        result_window.insert(tk.END, f"{i})\n")
        for member in combo:
            result_window.insert(tk.END, f"{member}\n")
        result_window.insert(tk.END, "-" * 20 + "\n")


# Создание окна
root = tk.Tk()
root.title('Формирование команд из отделов')

# Поля ввода
tk.Label(root, text='Количество в отделе продаж (k1):').grid(row=0, column=0)
entry_k1 = tk.Entry(root)
entry_k1.grid(row=0, column=1)

tk.Label(root, text='Количество в отделе маркетинга (k2):').grid(row=1, column=0)
entry_k2 = tk.Entry(root)
entry_k2.grid(row=1, column=1)

tk.Label(root, text='Размер команды (N):').grid(row=2, column=0)
entry_N = tk.Entry(root)
entry_N.grid(row=2, column=1)

tk.Label(root, text='Мин. количество из продаж:').grid(row=3, column=0)
entry_min_sales = tk.Entry(root)
entry_min_sales.grid(row=3, column=1)

# Кнопка запуска
generate_button = tk.Button(root, text='Сформировать комбинации', command=generate_combinations)
generate_button.grid(row=4, columnspan=2)

# Окно вывода с прокруткой
result_window = scrolledtext.ScrolledText(root, width=50, height=20)
result_window.grid(row=5, columnspan=2)

# Запуск приложения
root.mainloop()
