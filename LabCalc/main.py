'''
Лабораторная работа 2
Составить программу реализующую калькулятор.
Предусмотреть ввод с клавиатуры и с интерфейса.
Составить Меню:
    Повторение действий
    Очистка полей
    Информация об авторе и программе
Перевод в троичную систему счисления и обратно
    (Вещественные числа со знаком)
'''


def from3to10(x):
    '''
        Функция осуществляющая перевод из троичной СС
    в десятичную.
    '''
    negative = False # Флаг на отрицательные числа
    n = 3 # Основание СС
    # Отметка о отрицательности числа
    if x.count('-') == 1:
        x = x.replace('-', '')
        negative = True
    # Разделение на целую и дробную часть
    if x.count('.') == 1:
        decimal = x[:x.find('.')]
        fractional = x[x.find('.') + 1:]
    else:
        decimal = x
        fractional = None

    # Перевод десятичной части
    decimal10 = 0
    for i in range(len(decimal)):
        decimal10 += int(decimal[-i - 1]) * n**(i)
    # Перевод дробной части
    if fractional is not None:
        fractional10 = 0
        for i in range(len(fractional)):
            fractional10 += float(fractional[i]) * n**(-(i + 1))

        result = decimal10 + round(fractional10, 6)
        result = '{:.6f}'.format(result)
    else:
        result = decimal10
        result = '{:}'.format(result)

    if negative:
        result = '-' + result

    return result   


def from10to3(x):
    '''
        Функция осуществляющая перевод из десятичной СС
    в троичную.
    '''
    n = 3 # Основание системы счисления
    negative = False
    if x < 0:
        negative = True
        x = abs(x)
    if x >= 0 and x < 1:
        decimal_3 = '0'
    else:
        # Перевод целой части
        decimal = x // 1 # Целая часть

        decimal_3 = ''

        while decimal >= 1:
            decimal_3 = str(int(decimal % n)) + decimal_3
            decimal //= n
    
    if negative:
        decimal_3 = '-' + decimal_3
        
    # Перевод дробной части
    fractional = x % 1 # Дробная часть
    fractional_3 = ''
    if int(fractional * 1e6) != 0:
        for i in range(6): # Для кол-ва знаков после запятой = 6
            fractional *= n
            fractional_3 += str(int(fractional // 1))
            fractional %= 1

        result = decimal_3 + '.' + fractional_3
    else:
        result = decimal_3
    
    return result


import tkinter as tk
from tkinter import messagebox as mb

def clear():
    field.delete(0, 'end')


def show10():
    global base_flag
    error = 0
    if base_flag == 3 and len(field.get()) > 0:
        num = field.get()
        for i in num:
            if not num.isdigit:
                error = 1
                mb.showerror('Ошибка', 'Введены неверные данные')
                clear()
                break
        for i in ('3', '4', '5', '6', '7', '8', '9'):
            if num.count(i) > 0:
                error = 1
                mb.showerror('Ошибка', 'Введены неверные данные')
                clear()
                break
        while num.find('0') == 0:
            num = num[1:] 
        if error == 0:
            field.delete(0, tk.END)
            field.insert(0, from3to10(num))
            changeBase()
    else:
        pass


def show3():
    global base_flag
    error = 0
    if base_flag == 10 and len(field.get()) > 0:
        num = field.get()
        for i in num:
            if not i.isdigit():
                error = 1
                mb.showerror('Ошибка', 'Введены неверные данные')
                clear()
                break
        if error == 0:
            field.delete(0, tk.END)
            field.insert(0, from10to3(float(num)))
            changeBase()
    else:
        pass
    

def changeBase(): 
    global base_flag
    if base_flag == 10:
        base_flag = 3
    else:
        base_flag = 10
    menubar.entryconfig(7, label=('Осн: ' + str(base_flag)))


def transform():
    if base_flag == 10:
        show3()
    else:
        show10()


def makenegative():
    if len(field.get()) > 0 and field.get().count('-') == 0:
        field.insert(0,'-')


def makepositive():
    if len(field.get()) > 0 and field.get().count('-') == 1:
        field.delete(0, 1)

main = tk.Tk()
main.geometry()
main.title('Calculator')
# ------------------------------------------------------------ #
base_flag = 10
# ------------------------------------------------------------ #

# ------------------------------------------------------------ #
field = tk.Entry(main, width=16, font=("helvetica", 31), borderwidth=0)
field.grid(row=0, column=0, columnspan=4, padx=0, pady=0)
# ------------------------------------------------------------ #
button_7 = tk.Button(main, text='7', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=lambda:field.insert(len(field.get()),'7'))
button_7.grid(row=1, column=0, padx=0, pady=2)
# ------------------------------------------------------------ #
button_8 = tk.Button(main, text='8', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=lambda:field.insert(len(field.get()),'8'))
button_8.grid(row=1, column=1, padx=0, pady=2)
# ------------------------------------------------------------ #
button_9 = tk.Button(main, text='9', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=lambda:field.insert(len(field.get()),'9'))
button_9.grid(row=1, column=2, padx=0, pady=2)
# ------------------------------------------------------------ #
button_4 = tk.Button(main, text='4', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=lambda:field.insert(len(field.get()),'4'))
button_4.grid(row=2, column=0, padx=0, pady=2)
# ------------------------------------------------------------ #
button_5 = tk.Button(main, text='5', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=lambda:field.insert(len(field.get()),'5'))
button_5.grid(row=2, column=1, padx=0, pady=2)
# ------------------------------------------------------------ #
button_6 = tk.Button(main, text='6', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=lambda:field.insert(len(field.get()),'6'))
button_6.grid(row=2, column=2, padx=0, pady=2)
# ------------------------------------------------------------ #
button_1 = tk.Button(main, text='1', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=lambda:field.insert(len(field.get()),'1'))
button_1.grid(row=3, column=0, padx=0, pady=2)
# ------------------------------------------------------------ #
button_2 = tk.Button(main, text='2', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=lambda:field.insert(len(field.get()),'2'))
button_2.grid(row=3, column=1, padx=0, pady=2)
# ------------------------------------------------------------ #
button_3 = tk.Button(main, text='3', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=lambda:field.insert(len(field.get()),'3'))
button_3.grid(row=3, column=2, padx=0, pady=2)
# ------------------------------------------------------------ #
button_0 = tk.Button(main, text='0', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=lambda:field.insert(len(field.get()),'0'))
button_0.grid(row=4, column=1, padx=0, pady=2)
# ------------------------------------------------------------ #
button_dot = tk.Button(main, text='.', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=lambda:field.insert(len(field.get()),'.'))
button_dot.grid(row=4, column=2, padx=0, pady=2)
# ------------------------------------------------------------ #
button_dash = tk.Button(main, text='-', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=makenegative)
button_dash.grid(row=2, column=3, padx=0, pady=2)
# ------------------------------------------------------------ #
button_plus = tk.Button(main, text='+', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='grey', command=makepositive)
button_plus.grid(row=1, column=3, padx=0, pady=2)
# ------------------------------------------------------------ #
button_clear = tk.Button(main, text='C', width=3, height=1, font=("helvetica", 36), borderwidth=0, background='orange', command=clear)
button_clear.grid(row=4, column=0, padx=0, pady=2)
# ------------------------------------------------------------ #
button_10to3 = tk.Button(main, text='>>', width=3, height=3, font=("helvetica", 34), borderwidth=0, background='#73A1FF', command=transform)
button_10to3.grid(row=3, column=3, padx=0, pady=0, rowspan=2)
# ------------------------------------------------------------ #
# ------------------------------------------------------------ #
# -----------------------Menu--------------------------------- #
menubar = tk.Menu(main)


actionmenu = tk.Menu(menubar, tearoff=0)

actionmenu.add_command(label="Перевести из 10ой в 3ную", command=show3)
actionmenu.add_command(label="Перевести из 3ой в 10ную", command=show10)

menubar.add_cascade(label="Действия", menu=actionmenu)

menubar.add_command(label="Очистить", command=clear)
menubar.add_command(label="Информация", command=lambda:mb.showinfo("Информация о авторе и программе", '''
Автор: Шингаров Ильяс Девлетович
Ученик МГТУ им. Баумана, группы ИУ7-24Б
Программа сделана для лабораторной работы 2.
Реализован калькулятор осуществляющий перевод
из десятичной системы счисления в троичную и обратно
'''))
menubar.add_separator()
menubar.add_command(label="Выход", command=main.quit)
menubar.add_separator()
menubar.add_command(label=('Осн: ' + str(base_flag)), command=changeBase)

# ------------------------------------------------------------ #
main.config(menu=menubar)
# ------------------------------------------------------------ #



main.mainloop()