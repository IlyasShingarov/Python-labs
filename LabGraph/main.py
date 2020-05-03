import tkinter as tk
import tkinter.messagebox as mb
import math as m

def get_center(event):
    x = event.x
    y = event.y
    return x, y


def get_radius(event, x, y):
    rx = event.x
    ry = event.y
    return rx, ry


def mouse_circle(event):
    global circle_state
    global temp_coords
    if circle_state == 0:
        x, y = get_center(event)
        circle_state = 1
        temp_coords = (x, y)
    else:
        x, y = temp_coords
        rx, ry = get_radius(event, x, y)
        r = m.sqrt((rx - x)**2 + (ry - y)**2)
        circle = image.create_oval(x - r, y - r, x + r, y + r, width=circle_width, outline=circle_color)
        circle_state = 0
        
        circles.append((x, y, r))


def mouse_click(event):
    if mode_flag == 0:
        mouse_point(event)
    else:
        mouse_circle(event)


def mouse_point(event):
    x = event.x
    y = event.y
    points.append((x, y))

    p1x = x - point_radius
    p1y = y - point_radius
    p2x = x + point_radius
    p2y = y + point_radius

    point = image.create_oval(p1x, p1y, p2x, p2y, fill=point_color, width=point_width)


def changeFlag():
    global mode_flag

    if mode_flag == 0:
        mode_flag = 1
        menubar.entryconfig(3, label=('Режим: ' + 'Окружность'))
    else:
        menubar.entryconfig(3, label=('Режим: ' + 'Точка'))
        mode_flag = 0


def put_circle():

    try:
        x = int(circlex_entry.get())
        y = int(circley_entry.get())
        r = int(circler_entry.get())

        if x > 1000 or y > 900 or x < 0 or y < 0 or r < 1:
            mb.showerror("Ошибка", "Введены недопустимые данные")
            clear_circle()
    
        elif (x, y, r) not in circles:
            circles.append((x, y, r))

            p1x = x - r
            p1y = y - r

            p2x = x + r
            p2y = y + r

            circle = image.create_oval(p1x, p1y, p2x, p2y, width=circle_width, outline=circle_color)
    except ValueError:
        pass


def put_point():
    try:
        x = int(pointx_entry.get())
        y = int(pointy_entry.get())
        if x > 1000 or y> 1000 or x < 0 or y < 0:
            mb.showerror("Ошибка", "Введены недопустимые данные")
            clear_point()
        elif (x, y) not in points:
            points.append((x, y))

            p1x = x - point_radius
            p1y = y - point_radius

            p2x = x + point_radius
            p2y = y + point_radius

            point = image.create_oval(p1x, p1y, p2x, p2y, fill=point_color, width=point_width)
    except ValueError:
        pass


def clear_point():
    pointx_entry.delete(0, 'end')
    pointy_entry.delete(0, 'end')


def clear_circle():
    circlex_entry.delete(0, 'end')
    circley_entry.delete(0, 'end')
    circler_entry.delete(0, 'end')


def clear():
    circles.clear()
    points.clear()
    counted.clear()
    image.delete("all")

    dead = out_frame.grid_slaves()
    for d in dead:
        d.destroy()


def intersect(pointA, pointB, circle):
    distance = abs((pointA[1] - pointB[1]) * circle[0] + \
        (pointB[0] - pointA[0]) * circle[1] + \
            (pointA[0] * pointB[1] - pointA[1] * pointB[0]))/ \
                m.sqrt((pointA[1] - pointB[1])**2 + (pointB[0] - pointA[0])**2)
    
    return distance < circle[2]


def find_lines():
    if len(points) == len(circles) == 0:
        mb.showerror("Ошибка", "Плоскость пуста")
    elif len(points) < 2:
        mb.showerror("Ошибка", "Поставлено менее двух точек")
    elif len(circles) < 1:
        mb.showerror("Ошибка", "Нет ни одной окружности")
    else:
        for i in range(len(points) - 1):
            for j in range(i, len(points) - 1):
                counted.append(count_intersects(points[i], points[j + 1], circles))
        make_line()


def count_intersects(A, B, all_circles):
    counter = 0
    for C in all_circles:
        counter += intersect(A, B, C)

    return (A, B, counter)


def max_line(AB):
    return AB[2]


def make_line():
        AB = max(counted, key=max_line)
        image.create_line(AB[0][0], AB[0][1], AB[1][0], AB[1][1], fill="#530F40", width=line_width)
        print_lineinfo(AB)


def print_lineinfo(line):
    line_lable = tk.Label(out_frame, text="Линия проведена из точки А в точку B\n и пересекает окружности N раз", font=("helvetica", 16))
    line_lable.grid(row=0, columnspan=6)
    point_lable = tk.Label(out_frame, text="A:({};{})  B:({};{})  N:{}".format(line[0][0], line[0][1], line[1][0], line[1][1], line[2]), font=("helvetica", 16), bg="#89A1C9")
    point_lable.grid(row=1, columnspan=6)


circles = []
points = []
counted = []
temp_coords = ()

circle_state = 0
mode_flag = 0

point_radius = 3
point_width = 1
point_color = "#171F26"

circle_width = 2
circle_color = "#2C3740"

line_width = 2


# Инициализация основного окна
root = tk.Tk()
root.geometry()
root.resizable(0, 0)


# Инициализация фреймов для полей ввода и окна с графикой
input_frame = tk.Frame(root)
input_frame.grid(row=0, column=0, pady=0, sticky="w")

image_frame = tk.Frame(root)
image_frame.grid(row=0, column=1, rowspan=9, pady=0, sticky="w")

out_frame = tk.Frame(root)
out_frame.grid(row=2, column=0, pady=0, sticky="w")


# Создание полей ввода
# Поле ввода для точки
point_label = tk.Label(input_frame, text="Введите координаты точки", font=("helvetica", 16))
point_label.grid(row=0, column=0, columnspan=6)

x_label = tk.Label(input_frame, text="X:", font=("helvetica", 14))
x_label.grid(row=1, column=1, padx=0, pady=0, sticky="w")

pointx_entry = tk.Entry(input_frame, width='5', font=("helvetica", 14))
pointx_entry.grid(row=1, column=2, padx=0, pady=0, sticky="w")

y_label = tk.Label(input_frame, text="Y:", font=("helvetica", 14))
y_label.grid(row=1, column=3, padx=0, pady=0, sticky="w")

pointy_entry = tk.Entry(input_frame, width='5', font=("helvetica", 14))
pointy_entry.grid(row=1, column=4, padx=0, pady=0, sticky="w")
# Кнопка ввода
point_button = tk.Button(input_frame, text='Ввод', font=("helvetica", 18), width=26, height=2, borderwidth=0, bg="#8697A6", command=put_point)
point_button.grid(row=3, column=0, columnspan=6, padx=0, pady=10)


# Поле ввода окружности
circle_label = tk.Label(input_frame, text="Введите координаты центра\n и радиус окружности", font=("helvetica", 16))
circle_label.grid(row=4, column=0, columnspan=6)

cx_label = tk.Label(input_frame, text="X:", font=("helvetica", 14), padx=0, pady=0)
cx_label.grid(row=5, column=0, padx=0, pady=0)

circlex_entry = tk.Entry(input_frame, width='4', font=("helvetica", 14),)
circlex_entry.grid(row=5, column=1, padx=0, pady=0)

cy_label = tk.Label(input_frame, text="Y:", font=("helvetica", 14), padx=0, pady=0)
cy_label.grid(row=5, column=2, padx=0, pady=0)

circley_entry = tk.Entry(input_frame, width='4', font=("helvetica", 14))
circley_entry.grid(row=5, column=3, padx=0, pady=0)

cr_label = tk.Label(input_frame, text="R:", font=("helvetica", 14), padx=0, pady=0)
cr_label.grid(row=5, column=4, padx=0, pady=0)

circler_entry = tk.Entry(input_frame, width='4', font=("helvetica", 14))
circler_entry.grid(row=5, column=5, padx=0, pady=0)

# Кнопка ввода
circle_button = tk.Button(input_frame, text='Ввод', font=("helvetica", 18), width=26, height=2, borderwidth=0, bg="#8697A6", command=put_circle)
circle_button.grid(row=6, column=0, columnspan=6, padx=0, pady=10)

# Кнопка запуска основной функции
main_label = tk.Label(input_frame, text="Построить прямую, пересекающую\n максимальное кол-во окружностей", font=("helvetica", 16), padx=0, pady=0)
main_label.grid(row=7, column=0, columnspan=6)

main_button = tk.Button(input_frame, text='Найти', font=("helvetica", 18), width=26, height=2, borderwidth=0, bg="#8697A6", command=find_lines)
main_button.grid(row=8, column=0, columnspan=6, padx=0, pady=10)



# Меню
menubar = tk.Menu(root)

menubar.add_command(label="Информация", command=lambda:mb.showinfo("Информация о авторе и программе", '''
Автор: Шингаров Ильяс Девлетович
Ученик МГТУ им. Баумана, группы ИУ7-24Б
Программа сделана для лабораторной работы 4.
Программа позволяет отметить множество точек и окружностей на плоскости, после чего строит прямую, проходящую через две точки множетва и пересекающую наибольшее количество окружностей.
'''))
menubar.add_separator()
menubar.add_command(label=('Режим: ' + 'Точка'), command=changeFlag)
menubar.add_separator()
menubar.add_command(label=('Очистить холст'), command=clear)
menubar.add_separator()
menubar.add_command(label="Выход", command=root.quit)

root.config(menu=menubar)


# Настройки графического окна
image = tk.Canvas(image_frame, height=900, width=1000, bg="#BFCFD9")
image.bind('<Button-1>', mouse_click)
image.pack(pady=0)



root.mainloop()