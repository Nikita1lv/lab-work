import tkinter as tk
from tkinter import filedialog, messagebox
import math
from collections import defaultdict


# [КЛАСС 1]
class Tariff:
    def __init__(self, name, customer_type, service_type, price):
        self.name = name.strip()                      # [АТРИБУТ 1]
        self.customer_type = customer_type.strip()    # [АТРИБУТ 2]
        self.service_type = service_type.strip()      # [АТРИБУТ 3]
        try:
            self.price = float(str(price).replace(',', '.'))
        except Exception as e:
            raise ValueError(f"Цена должна быть числом, получено: {price}") from e
        if self.price < 0:
            raise ValueError("Цена не может быть отрицательной")

    def to_tuple(self):
        return (self.name, self.customer_type, self.service_type, self.price)


class TariffManager:
    CUSTOMER_TYPES = {"Физлицо", "ИП", "ООО", "Госучреждение"}
    SERVICE_TYPES = {"Звонки", "Интернет", "SMS", "Роуминг", "Пакет"}

    def __init__(self):
        self.tariffs = []
        self.errors = []

    def _split_line(self, line):
        line = line.strip()
        if not line or line.startswith('#'):
            return None
        return [p.strip() for p in line.split(',')] if ',' in line else line.split()

    def load_from_file(self, path):  # [МЕТОД 1/4]
        self.tariffs.clear()
        self.errors.clear()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for i, raw in enumerate(f, start=1):
                    parts = self._split_line(raw)
                    if parts is None:
                        continue
                    if parts[0].lower() in ("name", "название"):
                        continue
                    if len(parts) < 4:
                        self.errors.append(f"Строка {i}: мало столбцов (ожидалось >=4).")
                        continue
                    name, customer, service, price = parts[0], parts[1], parts[2], parts[3]
                    if customer not in self.CUSTOMER_TYPES:
                        allowed = ", ".join(sorted(self.CUSTOMER_TYPES))
                        self.errors.append(f"Строка {i}: неизвестный тип заказчика '{customer}'. Допустимо: {allowed}")
                        continue
                    if service not in self.SERVICE_TYPES:
                        allowed = ", ".join(sorted(self.SERVICE_TYPES))
                        self.errors.append(f"Строка {i}: неизвестный вид услуги '{service}'. Допустимо: {allowed}")
                        continue
                    try:
                        tariff = Tariff(name, customer, service, price)
                    except ValueError as e:
                        self.errors.append(f"Строка {i}: {e}")
                        continue
                    self.tariffs.append(tariff)
        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Не удалось прочитать файл: {e}")

    def segment_by_customer(self):  # [МЕТОД 2/4]
        counts = defaultdict(int)
        for t in self.tariffs:
            counts[t.customer_type] += 1
        return dict(counts)

    def segment_by_service(self):  # [МЕТОД 3/4]
        counts = defaultdict(int)
        for t in self.tariffs:
            counts[t.service_type] += 1
        return dict(counts)

    def total(self):  # [МЕТОД 4/4]
        return len(self.tariffs)


class PieChartCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg='white', highlightthickness=0)

    def draw_pie(self, data, title=""):
        self.delete("all")
        w, h = int(self['width']), int(self['height'])
        top_margin = 56 if title else 16
        side_margin = 24
        bottom_margin = 20
        if title:
            self.create_rectangle(0, 0, w, top_margin, fill="#eef3ff", outline="")
            self.create_text(w//2, top_margin//2, text=title, font=("Arial", 16, "bold"), fill="#2c3e50")
        cx = side_margin + (w - 2*side_margin)//2
        cy = top_margin + (h - top_margin - bottom_margin)//2
        r = max(10, min((w - 2*side_margin), (h - top_margin - bottom_margin))//2 - 6)
        bbox = (cx - r, cy - r, cx + r, cy + r)
        total = sum(v for v in data.values() if v > 0) or 1
        start_angle = 0.0
        palette = ["#4e79a7","#f28e2b","#e15759","#76b7b2","#59a14f","#edc948","#b07aa1","#ff9da7","#9c755f","#bab0ab"]
        legend_x = cx + r + 24
        legend_y = top_margin + 6
        self.create_text(legend_x, legend_y-4, anchor="nw", text="Легенда", font=("Arial", 11, "bold"), fill="#34495e")
        for idx, (label, value) in enumerate(sorted(data.items(), key=lambda kv: -kv[1])):
            if value <= 0:
                continue
            extent = 360.0 * (value / total)
            color = palette[idx % len(palette)]
            self.create_arc(bbox, start=start_angle, extent=extent, fill=color, outline="white", width=2)
            mid = start_angle + extent/2.0
            rad = math.radians(mid)
            tx = cx + math.cos(rad) * (r * 0.58)
            ty = cy - math.sin(rad) * (r * 0.58)
            percent = (value / total) * 100
            self.create_text(tx, ty, text=f"{label}\n{value} ({percent:.1f}%)", font=("Arial", 9), justify="center", fill="#1f2d3d")
            row_y = legend_y + 18 + idx * 22
            self.create_rectangle(legend_x, row_y, legend_x + 16, row_y + 16, fill=color, outline=color)
            self.create_text(legend_x + 22, row_y + 8, anchor="w", text=f"{label}: {value}", font=("Arial", 10), fill="#2c3e50")
            start_angle += extent


class TariffApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Телефонные тарифы — сегментация и диаграммы (Tkinter)")
        self.manager = TariffManager()
        left = tk.Frame(root)
        left.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        right = tk.Frame(root)
        right.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)
        self.log = tk.Text(left, width=44, height=28, state="disabled", bg="#f7f8fa", relief="flat")
        self.log.pack(fill="both", expand=True)
        btns = tk.Frame(left)
        btns.pack(fill="x", pady=(6,0))
        tk.Button(btns, text="Загрузить файл...", command=self.load_file, bg="#4e79a7", fg="white", activebackground="#3e648a", relief="flat", padx=10, pady=6).pack(side="left", padx=3)
        toolbar = tk.Frame(right, bg="#eef3ff")
        toolbar.pack(fill="x")
        tk.Label(toolbar, text="Визуализация:", bg="#eef3ff", fg="#2c3e50", font=("Arial", 10, "bold")).pack(side="left", padx=(10,6), pady=6)
        tk.Button(toolbar, text="По заказчикам", command=self.show_by_customer, bg="#59a14f", fg="white", activebackground="#4b8a43", relief="flat", padx=10, pady=6).pack(side="left", padx=4, pady=6)
        tk.Button(toolbar, text="По видам услуг", command=self.show_by_service, bg="#f28e2b", fg="white", activebackground="#cf7516", relief="flat", padx=10, pady=6).pack(side="left", padx=4, pady=6)
        self.canvas = PieChartCanvas(right, width=760, height=520)
        self.canvas.pack(fill="both", expand=True)
        self.status = tk.Label(root, anchor="w", text="Файл не загружен", bg="#ffffff")
        self.status.grid(row=1, column=0, columnspan=2, sticky="ew", padx=6, pady=(0,6))

    def load_file(self):
        path = filedialog.askopenfilename(title="Выберите файл тарифов", filetypes=[("CSV и TXT", "*.csv *.txt"), ("Все файлы", "*.*")])
        if not path:
            return
        try:
            self.manager.load_from_file(path)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл не найден")
            return
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            return
        ok = self.manager.total()
        errs = len(self.manager.errors)
        self._log_clear()
        self._log_write(f"Загружено валидных тарифов: {ok}\nОшибок: {errs}\n\n")
        for e in self.manager.errors[:100]:
            self._log_write("- " + e + "\n")
        self.status.config(text=f"Загружено: {ok} тарифов. Ошибок: {errs}")
        if ok == 0:
            self.canvas.delete("all")
            messagebox.showwarning("Внимание", "Не удалось загрузить ни одного корректного тарифа")

    def show_by_customer(self):
        if self.manager.total() == 0:
            messagebox.showinfo("Нет данных", "Сначала загрузите файл с тарифами")
            return
        data = self.manager.segment_by_customer()
        self._log_distribution("Распределение по заказчикам", data)
        self.canvas.draw_pie(data, title="Сегментация по заказчикам")

    def show_by_service(self):
        if self.manager.total() == 0:
            messagebox.showinfo("Нет данных", "Сначала загрузите файл с тарифами")
            return
        data = self.manager.segment_by_service()
        self._log_distribution("Распределение по видам услуг", data)
        self.canvas.draw_pie(data, title="Сегментация по видам услуг")

    def _log_clear(self):
        self.log.config(state="normal")
        self.log.delete("1.0", tk.END)
        self.log.config(state="disabled")

    def _log_write(self, text):
        self.log.config(state="normal")
        self.log.insert(tk.END, text)
        self.log.config(state="disabled")

    def _log_distribution(self, title, data):
        total = sum(data.values()) or 1
        self._log_write(title + "\n")
        for k, v in sorted(data.items(), key=lambda kv: -kv[1]):
            pct = 100.0 * v / total
            self._log_write(f"  {k:<15} : {v:>3}  ({pct:5.1f}%)\n")
        self._log_write("\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = TariffApp(root)
    root.mainloop()
