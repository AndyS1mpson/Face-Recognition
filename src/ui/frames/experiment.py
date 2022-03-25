from tkinter import BOTH, HORIZONTAL, RIGHT, VERTICAL, Button, Canvas, Entry, Frame, Label, OptionMenu, Scrollbar, StringVar

from core.config.config import ALL_METHODS
from core.recognition import recognition
from PIL import Image, ImageTk
import random

class ExperimentFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Скролбары

        self.canvas = Canvas(self, width=1000, height=900)
        #self.scroll_y = Scrollbar(self.canvas, orient=VERTICAL)
        #self.scroll_y.grid(column=20)
        self.canvas.grid(row=3, column=5, padx=15, pady=7)
        #self.canvas.config(yscrollcommand=self.scroll_y.set, scrollregion=self.canvas.bbox("all"))
        #self.scroll_y.config(command=self.canvas.yview)
        # Метод извлечения признаков
        self.method_label = Label(self, text="Параметр")
        self.method_label.grid(row=0, column=0, padx=15, pady=7)

        self.method = StringVar()
        self.method.set(ALL_METHODS[1])

        self.method_drop = OptionMenu(self, self.method, *ALL_METHODS)
        self.method_drop.configure(width=10)
        self.method_drop.grid(row=1, column=0, padx=15, pady=7)     

        # Параметр метода
        self.param_label = Label(self, text="Параметр")
        self.param_label.grid(row=0, column=1, padx=15, pady=7)
        self.p_entry = Entry(self, width=7)
        self.p_entry.grid(row=1, column=1, padx=15, pady=7)    

        # Номер, с которого будут браться шаблоны для каждого человека
        self.from_templ_label = Label(self, text="С")
        self.from_templ_label.grid(row=0, column=2, padx=15, pady=7)
        self.from_template_entry = Entry(self, width=7)
        self.from_template_entry.grid(row=1, column=2, padx=15, pady=7)

        # Номер, по который будут браться шаблоны для каждого человека
        self.to_templ_label = Label(self, text="По")
        self.to_templ_label.grid(row=0, column=3, padx=15, pady=7)
        self.to_template_entry = Entry(self, width=7)
        self.to_template_entry.grid(row=1, column=3, padx=15, pady=7)
    
        self.score_label = Label(self, text="Точность:")
        self.score_label.grid(row=1, column=4, pady=10, sticky='E')
        self.score_result = Label(self, text="")
        self.score_result.grid(row=1, column=5, pady=10, sticky='W')

        # Список классифицируемых изображений
        self.result_images = []
        # Список содержащий по шаблону для каждого из классифицируемых изображений
        self.templates = []


        # Запуск исследования

        self.run_but = Button(
            self, 
            text="Запустить",
            command=lambda: self.show_result()
        )
        self.run_but.grid(row=2, column=1, padx=15, pady=7)




    def show_result(self):
        score, images, templates = recognition(
            'ORL',
            #research_method.get(),
            self.method.get(),
            int(self.p_entry.get()),
            int(self.from_template_entry.get()),
            int(self.to_template_entry.get())
        )
        self.score_result.config(text=score)

        templ_posx = 50
        templ_posy = 50

        res_posx = 300
        res_posy = 50

        random_indexes = [random.randrange(len(images)) for _ in range(5)]


        for index in random_indexes:
            templ = Image.fromarray(templates[index])
            templ.resize((50, 50))
            templ = ImageTk.PhotoImage(templ)
            self.templates.append(templ)
            self.canvas.create_image(templ_posx, templ_posy, image=templ)
                
            templ_posy += 80

            img=Image.fromarray(images[index])
            img.resize((50, 50))
            img = ImageTk.PhotoImage(img)
            self.result_images.append(img)
            self.canvas.create_image(res_posx, res_posy, image=img)

            res_posy += 80
