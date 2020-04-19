# Лабораторная работа 3. Сортировка массива.

#---------------------------------------------------------------------------------#
from tkinter import ttk
import tkinter as tk

from time import perf_counter

from random import randint

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
#---------------------------------------------------------------------------------#

def gnome_sort(array):
    i, j = 1, 2
    length = len(array)

    t1 = perf_counter()
    while i < length:
        if array[i - 1] <= array[i]:
            i, j = j, j + 1
        else:
            array[i - 1], array[i] = array[i], array[i - 1]
            i -= 1
            if i == 0:
                i, j = j, j + 1
    t2 = perf_counter()

    return t2 - t1


def sorted_array_init(n):
    a = []
    for i in range(n):
        a.append(i)
    return a


def random_array_init(n):
    a = []
    for i in range(n):
        a.append(randint(10,99))
    return a


def inverted_sorted_array(n):
    a = []
    for i in range(n, -1, -1):
        a.append(i)
    return a

N = 10

#---------------------------------------------------------------------------------#
# Main
main = tk.Tk()
main.title("Сортировка массива")
main.geometry()

# Example
example_frame = tk.Frame(main)
example_frame.grid(row=0, column=0)

# Temp output
example_label = tk.Label(example_frame, text="Исходный массив:", font=("helvetica", 19), background="#456A72", width='16', borderwidth=3)
example_label.grid(row=0, column=0, sticky="nw")

array = random_array_init(N)
for i in range(1, N + 1):
    label = tk.Label(example_frame, text=str(array[i - 1]), font=("helvetica", 19), padx=5, background='#8EA1A5', borderwidth=3)
    label.grid(row=0, column=i, sticky="nw")

sorted_example_label = tk.Label(example_frame, text="Отсортированный:", font=("helvetica", 19), background="#456A72", width='16', borderwidth=3)
sorted_example_label.grid(row=1, column=0, sticky="nw")

gnome_sort(array)
for i in range(1, N + 1):
    label = tk.Label(example_frame, text=str(array[i - 1]), font=("helvetica", 19), padx=5, background='#8EA1A5', borderwidth=3)
    label.grid(row=1, column=i, sticky="nw")

#Table
table_frame = tk.Frame(main)
table_frame.grid(row=1, column=0)

style = ttk.Style(table_frame)
#style.theme_use("clam")
style.configure("Treeview", background="#8EA1A5", 
                fieldbackground="#8EA1A5")


table = ttk.Treeview(table_frame, columns = ['N1', 'N2', 'N3'], height=3, selectmode='none')
table.heading('#0', text = 'Массив')
table.heading('N1', text = '100')
table.heading('N2', text = '500')
table.heading('N3', text = '1000')
table.column('#0', width = 200, anchor = 'center')
table.column('N1', width = 162, anchor = 'center')
table.column('N2', width = 162, anchor = 'center')
table.column('N3', width = 161, anchor = 'center')

# Count time
array = random_array_init(100)
t1 = round(gnome_sort(array),6)
array = random_array_init(500)
t2 = round(gnome_sort(array),6)
array = random_array_init(1000)
t3 = round(gnome_sort(array),6)
table.insert('',1,text = 'Случайный', values = (t1, t2, t3))

array = sorted_array_init(100)
t1 = round(gnome_sort(array),6)
array = sorted_array_init(500)
t2 = round(gnome_sort(array),6)
array = sorted_array_init(1000)
t3 = round(gnome_sort(array),6)
table.insert('',2,text = 'Упорядоченный', values = (t1, t2, t3))

array = inverted_sorted_array(100)
t1 = round(gnome_sort(array),6)
array = inverted_sorted_array(500)
t2 = round(gnome_sort(array),6)
array = inverted_sorted_array(1000)
t3 = round(gnome_sort(array),6)
table.insert('',3,text = 'Упорядоченный (обратный)', values = (t1, t2, t3))

table.grid()

# Plot

plot_frame = tk.Frame(main)
plot_frame.grid(row=3, column=0)

x = []
y = []
for i in range(1000, 6000, 500):
    x.append(i)
    a = random_array_init(i)
    t = gnome_sort(a)
    y.append(t)


figure = Figure(figsize=(9,7), dpi=75)
ax = figure.add_subplot(111)
ax.set_xlabel('Кол-во элементов', fontsize=18)
ax.set_ylabel('Вермя', fontsize=18)
ax.set_title('Зависимость времени сортировки от размера массива', fontsize=18)
ax.axis([900, 5600, min(y) - 0.5, max(y) + 0.5])

ax.grid()
func_line, = ax.plot(x, y)

canvas = FigureCanvasTkAgg(figure, plot_frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2Tk(canvas, plot_frame)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

main.mainloop()
input()