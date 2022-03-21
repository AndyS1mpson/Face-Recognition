from tkinter import (Button, Entry, IntVar, Label, OptionMenu, StringVar, Tk,
                     ttk)

from PIL import Image, ImageTk

from core.config.config import ALL_METHODS, RESEARCHES, RESULT
from core.research import research_1_N


def show_result():
    global result_image
    research_1_N(
        'ORL',
        #research_method.get(),
        method.get(),
        int(template_entry.get())
        #param.get()
    )
    result = Image.open(RESULT.format(im='param_plot'))
    result = result.resize((400, 400))
    result_image = ImageTk.PhotoImage(result)
    result_label = Label(research_tab, image=result_image)
    result_label.grid(row=3, column=0, padx=15, pady=10)   



window = Tk()
window.title = "Face Recognition"
window.geometry("1000x900")

# Настройка вкладок

tab_parent = ttk.Notebook(window)

research_tab = ttk.Frame(tab_parent)
ex_tab = ttk.Frame(tab_parent)

tab_parent.add(research_tab, text="Исследование")
tab_parent.add(ex_tab, text="Параллельная система")
tab_parent.pack(expand=1, fill='both')

# Dropdown для выбора метода

method = StringVar()
method.set(ALL_METHODS[1])

method_label = Label(research_tab, text="Метод")
method_label.grid(row=0, column=0, padx=15, pady=7)
method_drop = OptionMenu(research_tab, method, *ALL_METHODS)
method_drop.configure(width=20)
method_drop.grid(row=1, column=0, padx=15, pady=7)

# Dropdown для выбора исследования

research_method = StringVar()
research_method.set(RESEARCHES[0])

research_label = Label(research_tab, text="Исследование")
research_label.grid(row=0, column=1, padx=15, pady=7)
research_drop = OptionMenu(research_tab, research_method, *RESEARCHES)
research_drop.configure(width=20)
research_drop.grid(row=1, column=1, padx=15, pady=7)

# Параметр метода

param = IntVar()
param_label = Label(research_tab, text="Параметр")
param_label.grid(row=0, column=2, padx=15, pady=7)
p_entry = Entry(research_tab)
p_entry.grid(row=1, column=2, padx=15, pady=7)

# Выбор фото для шаблона
#template_num = IntVar()
template_label = Label(research_tab, text="Номер шаблона")
template_label.grid(row=0, column=3, padx=15, pady=7)
template_entry = Entry(research_tab)
template_entry.grid(row=1, column=3, padx=15, pady=7)
# Запуск исследования

run_but = Button(
    research_tab, 
    text="Запустить",
    command=lambda: show_result()
)
run_but.grid(row=2, column=1, padx=15, pady=7)

# Запуск приложения
window.mainloop()
