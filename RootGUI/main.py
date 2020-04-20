# Лабораторная работа №1 (2 семестр)
# Шингаров Ильяс ИУ7-24Б

# Plotting
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

# Calculation
import numpy as np

# GUI
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb

# Initial functions
def f(x):
    return eval(in_f.get())

# Chords method step
def chords(a, b):
    '''
    Метод хорд
    Функция соверщает одну итерацию метода хорд,
    возвращая пересечение х
    '''

    fb = f(b)
    xn = a - f(a) * (b - a) / (fb - f(a))
    return xn


# Refinement function
def refine(a, b, h, eps):
    '''
    Уточняет корень на промежутке от a до b
    C шагом h, точностью eps
    Возвращает массив словарей, 
    содержащий данные для таблицы

    '''

    num = 0 # Номер интервала
    x1 = a # Начало промежутка
    data = [] # Массив для хранения выходных данных

    # Поиск корня на интервале (a, b) с шагом h
    while x1 < b:
        num += 1

        # Разбиение на участки
        if x1 + h <= b:
            x2 = x1 + h
        else:
            x2 = b

        # Округление пренебрежимо малых значений
        if abs(x1) < 1e-16:
            x1 = float(0)
        if abs(x2) < 1e-16:
            x2 = float(0)

        # Значение функции на концах отрезка должны иметь разные знаки
        if f(x1)*f(x2) < 0:
            
            # Определение первого приближения методом хорд
            x = chords(x1, x2)
            x_previous = x1 # Предыдущее приблежение
            iteration = 0 # Cчетчик кол-ва итераций
            error = '-' # Код ошибки

            while abs(x - x_previous) >= eps:
                # Вычисление нового приближения x
                iteration += 1
                t = x
                x = chords(x, x_previous)
                x_previous = t

            # Запись массива словарей со значениями
            data.append({
                'a': x1,
                'b': x2,
                'error': error,
                'root': x,
                'iteration': iteration,
            })
        
        # Корень на границе интервала
        elif f(x1) * f(x2) <= 1e-8:
            #error = '1'
            error = '-'
            iteration = '-'
            if abs(f(x1)) <= 1e-8:
                x = x1
            else:
                x = x2
            
            # Запись массива словарей со значениями
            data.append({
                    'a': x1,
                    'b': x2,
                    'error': error,
                    'root': x,
                    'iteration': iteration,
                })
                
            if abs(f(x2)) <= 1e-8:
                x1 += h

        x1 += h # Шаг

    return data


# Input data check
def check():
    try:
        a = float(in_a.get())
        b = float(in_b.get())
        h = float(in_h.get())
        eps = float(in_eps.get())
    except ValueError:
        mb.showerror('Ошибка','Неверные данные')
    else:
        dead = table_frame.pack_slaves()
        for d in dead:
            d.destroy()
        
        dead = plot_frame.pack_slaves()
        for d in dead:
            d.destroy()
        
        table(table_frame, refine(a, b, h, eps))
        f_plot(plot_frame, a, b)


# Table print
def table(table_frame, data):
    '''
    Функция выводящяя таблицу значений

    №Интервала|Интервал|Знач. корня|Знач. функции|Кол-во итераций|Код ошибки

    '''
    table = ttk.Treeview(table_frame, selectmode='none')
    scroll = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)

    table.configure(yscrollcommand=scroll.set)
    
    table["columns"] = ("1", "2", "3", "4", "5", "6")
    table['show'] = 'headings'
    table.column("1", anchor='e')
    table.column("2", anchor='e')
    table.column("3", anchor='e')
    table.column("4", anchor='e')
    table.column("5", anchor='e')
    table.column("6", anchor='e')
    table.heading("1", text="№")
    table.heading("2", text="Отрезок")
    table.heading("3", text="Корень")
    table.heading("4", text="Значение")
    table.heading("5", text="Итерации")
    table.heading("6", text="Ошибка")
    
    table.pack(side=tk.LEFT, fill=tk.BOTH)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    for i, result in enumerate(data, start=1):
        table.insert("", 'end', text=i, values=(
            i,
            "[{:.4f};{:.4f}]".format(result["a"], result["b"]),
            "{:.7f}".format(result["root"]),
            "{:.0e}".format(f(result["root"])),
            result["iteration"],
            result["error"],
        ))


# Clear data
def update():
    in_a.delete(0, 'end')
    in_b.delete(0, 'end')
    in_h.delete(0, 'end')
    in_eps.delete(0, 'end')
    
    dead = table_frame.pack_slaves()
    for d in dead:
        d.destroy()

    dead = plot_frame.pack_slaves()
    for d in dead:
        d.destroy()

    main.geometry("150x405")


# Plot function
def f_plot(plot_frame, start, end):
    # sampling
    samples = 500 # Samles for graph
    derivative_samples = 50000 # Samles for derivative

    x_scale_max = abs(max(start, end)) + 1
    x_scale_min = abs(min(start, end)) + 1
                      
    # Graphing info
    x = np.linspace(start, end, samples)
    y = f(x)

    y_scale_max = abs(max(y)) + 1
    y_scale_min = abs(min(y)) + 1

    # Derivative info
    dx = np.linspace(start, end, derivative_samples)

    dy = f(dx)
    dy = np.diff(dy)
    dy = np.insert(dy, 0, dy[0])
    dy /= ((end - (start)) / derivative_samples)


    # Derivative graphing
    crit_x = []
    der_zeros_nums = []

    for n in range(1, derivative_samples): # find number of critical point
        if (dy[n - 1] * dy[n]) <= 0:
            der_zeros_nums.append(n)

    for n in der_zeros_nums: # arrange critical x values
        elem = start + ((end - start) / derivative_samples) * n
        crit_x.append(elem)

    crit_y = []
    for i in crit_x: # arrange critical y values
        crit_y.append(f(i))


    # Plotting
    figure = Figure(figsize=(14,7), dpi=75)
    ax = figure.add_subplot(111)
    ax.set_xlabel('x', fontsize=18)
    ax.set_ylabel('y = f(x)', fontsize=18)
    ax.set_title('Function plot', fontsize=18)

    ax.plot(x,x*0, color='black', label='X axis')

    ax.axis([-x_scale_min, x_scale_max, -y_scale_min, y_scale_max]) # Square plot
    func_line, = ax.plot(x, y, label='Function graph')
    ax.grid()
    ax.scatter(crit_x, crit_y, color='red', label='Extremum') # Critical points scatterplot
# ------------------------------------------------------------------------------ #
    idx = np.argwhere(np.diff(np.sign(f(dx) - dx*0))).flatten()
    ax.plot(dx[idx], f(dx)[idx], 'yo', label='Root')

    ax.legend()
# ------------------------------------------------------------------------------ #

    canvas = FigureCanvasTkAgg(figure, plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2Tk(canvas, plot_frame)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


# Main body
main = tk.Tk()
main.geometry()
main.title("Уточнение корней")

# Input frame
data_in = tk.Frame(main)
data_in.grid(row=0, column=0, sticky='nw')

# Table frame
table_frame = tk.Frame(main)
table_frame.grid(row=1, column=0, columnspan=2, sticky='sw')

# Plot frame
plot_frame = tk.Frame(main)
plot_frame.grid(row=0, column=1, sticky='ne')


# ---------------------------------------------------------------- #
# Ввод функци
f_label = tk.Label(data_in, text="Функция", font=("helvetica", 14))
f_label.grid(row=0, column=0, padx=2, pady=2)

in_f = tk.Entry(data_in, width=16, font=("helvetica", 14))
in_f.grid(row=1, column=0, padx=2, pady=2)
# ---------------------------------------------------------------- #
# Подпись над полем ввода правой границы
a_label = tk.Label(data_in, text="Начало отрезка", font=("helvetica", 14))
a_label.grid(row=2, column=0, padx=2, pady=2)

# Поле ввода переменной "а" -- правой границы интервала
in_a = tk.Entry(data_in, width=12, font=("helvetica", 14))
in_a.grid(row=3, column=0, padx=2, pady=2)

# Подпись над полем ввода левой границы
b_label = tk.Label(data_in, text="Конец отрезка", font=("helvetica", 14))
b_label.grid(row=4, column=0, padx=2, pady=2)

# Поле ввода переменной 'b' -- левой границы интервала
in_b = tk.Entry(data_in, width=12, font=("helvetica", 14))
in_b.grid(row=5, column=0, padx=2, pady=2)

# Подпись над полем ввода шага
h_label = tk.Label(data_in, text="Шаг", font=("helvetica", 14))
h_label.grid(row=6, column=0, padx=2, pady=2)

# Поле ввода шага
in_h = tk.Entry(data_in, width=12, font=("helvetica", 14))
in_h.grid(row=7, column=0, padx=2, pady=4)

# Подпись поля ввода точности
eps_label = tk.Label(data_in, text="Точность", font=("helvetica", 14))
eps_label.grid(row=8, column=0, padx=2, pady=2)

# Поле ввода точности
in_eps = tk.Entry(data_in, width=12, font=("helvetica", 14))
in_eps.grid(row=9, column=0, padx=2, pady=6)
# ---------------------------------------------------------------- #

# Кнопка ввода и запуска основной программы
btn = tk.Button(data_in, text='Ввод', width=20, borderwidth='2', background ='grey', height=2, command=lambda:check())
btn.grid(row=10, column=0)

clear_button = tk.Button(data_in, text='Очистить', width=20, borderwidth='2', background ='grey', height=2, command=lambda:update())
clear_button.grid(row=11, column=0)

# ---------------------------------------------------------------- #

'''
error_label = tk.Label(data_in, text='Код ошибки:\n 1 - Корень на границе')
error_label.grid(row=12, column=0)
'''

main.mainloop()
