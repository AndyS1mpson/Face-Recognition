import random
from tkinter import (LEFT, TOP, Button, Canvas, Entry, Frame, Label,
                     OptionMenu, StringVar, W)

from core.config.config import ALL_METHODS, DATA_PATH
from core.recognition import parallel_recognition, recognition
from PIL import Image, ImageTk


class ExperimentFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.consistent_frame = Frame(self)
        self.parallel_frame = Frame(self)
        self.canvas_frame = Frame(self)

    # =============== ПОСЛЕДОВАТЕЛЬНАЯ СИСТЕМА ===============

        self.cons_label = Label(
            self.consistent_frame,
            text="Последовательная система",
            font='Times 15'
        )

        self.method_label = Label(self.consistent_frame, text="Метод: ")

        self.method = StringVar()
        self.method.set(ALL_METHODS[1])
        self.method_drop = OptionMenu(
            self.consistent_frame,
            self.method,
            *ALL_METHODS
        )
        self.method_drop.configure(width=10)

        # Параметр метода
        self.param_label = Label(self.consistent_frame, text="Параметр: ")
        self.p_entry = Entry(self.consistent_frame, width=7)

        # Номер, с которого будут браться шаблоны для каждого человека
        self.from_templ_label = Label(self.consistent_frame, text="С: ")
        self.from_template_entry = Entry(self.consistent_frame, width=7)

        # Номер, по который будут браться шаблоны для каждого человека
        self.to_templ_label = Label(self.consistent_frame, text="По: ")
        self.to_template_entry = Entry(self.consistent_frame, width=7)
        self.score_label = Label(self.consistent_frame, text="Точность:")
        self.score_result = Label(self.consistent_frame, text="")

        # Список классифицируемых изображений
        self.result_images = []

        # Список содержащий по шаблону для
        # каждого из классифицируемых изображений
        self.templates = []

        # Запуск исследования
        self.run_but = Button(
            self.consistent_frame,
            text="Запустить",
            command=lambda: self.consistent_experiment()
        )

    # =============== ПАРАЛЛЕЛЬНАЯ СИСТЕМА ===============
        self.parallel_label = Label(
            self.parallel_frame,
            text="Параллельная система",
            font='Times 15'
        )

        # ПАРАМЕТРЫ

        # Histogram
        self.hist_label = Label(self.parallel_frame, text="Histogram: ")
        self.hist_entry = Entry(self.parallel_frame, width=7)

        # Scale
        self.scale_label = Label(self.parallel_frame, text="Scale: ")
        self.scale_entry = Entry(self.parallel_frame, width=7)

        # Gradient
        self.gradient_label = Label(self.parallel_frame, text="Gradient: ")
        self.gradient_entry = Entry(self.parallel_frame, width=7)

        # DFT
        self.dft_label = Label(self.parallel_frame, text="DFT: ")
        self.dft_entry = Entry(self.parallel_frame, width=7)

        # DCT
        self.dct_label = Label(self.parallel_frame, text="DCT: ")
        self.dct_entry = Entry(self.parallel_frame, width=7)

        # Число шаблонов
        self.templ_num_label = Label(self.parallel_frame, text="L: ")
        self.templ_num_entry = Entry(self.parallel_frame, width=7)

        # Запуск параллельного исследования
        self.parallel_button = Button(
            self.parallel_frame,
            text="Запустить",
            command=lambda: self.parallel_experiment()
        )

        self.canvas = Canvas(self.canvas_frame, width=1000, height=900)

    # =============== МЕСТОПОЛОЖЕНИЕ ВИДЖЕТОВ ===============

        self.consistent_frame.pack(side=TOP, anchor=W)
        self.parallel_frame.pack(side=TOP, anchor=W)
        self.canvas_frame.pack(side=TOP, anchor=W)

        # Настройка фрейма для последовательной системы
        self.cons_label.pack(side=TOP, padx=10, pady=7, anchor=W)
        self.method_label.pack(side=LEFT, anchor=W, padx=10, pady=7)
        self.method_drop.pack(side=LEFT, anchor=W, padx=10, pady=7)

        self.param_label.pack(side=LEFT, anchor=W, padx=10, pady=7)
        self.p_entry.pack(side=LEFT, anchor=W, padx=10, pady=7)

        self.from_templ_label.pack(side=LEFT, anchor=W, padx=10, pady=7)
        self.from_template_entry.pack(side=LEFT, anchor=W, padx=10, pady=7)

        self.to_templ_label.pack(side=LEFT, anchor=W, padx=10, pady=7)
        self.to_template_entry.pack(side=LEFT, anchor=W, padx=10, pady=7)

        self.run_but.pack(side=LEFT, anchor=W, padx=10, pady=7)

        self.score_label.pack(side=LEFT, anchor=W, padx=10)
        self.score_result.pack(side=LEFT, anchor=W)

        # Настройка фрейма для параллельной системы
        self.parallel_label.pack(side=TOP, padx=10, pady=7, anchor=W)
        self.hist_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.hist_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.scale_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.scale_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.gradient_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.gradient_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.dft_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.dft_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.dct_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.dct_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.templ_num_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.templ_num_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.parallel_button.pack(side=TOP, padx=10, pady=7, anchor=W)

        # Настройка фрейма с Canvas
        self.canvas.pack(side=TOP)

    def consistent_experiment(self) -> None:
        """
        Проведение эксперимента с последовательной системой
        и отображение результатов.
        """
        score, images, templates = recognition(
            "ORL",
            # research_method.get(),
            self.method.get(),
            int(self.p_entry.get()),
            int(self.from_template_entry.get()),
            int(self.to_template_entry.get()),
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

            img = Image.fromarray(images[index])
            img.resize((50, 50))
            img = ImageTk.PhotoImage(img)
            self.result_images.append(img)
            self.canvas.create_image(res_posx, res_posy, image=img)

            res_posy += 80

    def parallel_experiment(self) -> None:
        """
        Проведение эксперимента с параллельной системой
        и отображение результатов.
        """
        params = [
            ('hist', int(self.hist_entry.get())),
            ('scale', int(self.scale_entry.get())),
            ('grad', int(self.gradient_entry.get())),
            ('dft', int(self.dft_entry.get())),
            ('dct', int(self.dct_entry.get()))
        ]
        L = int(self.templ_num_entry.get())
        scores = parallel_recognition(
            db_name='ORL',
            params=params,
            templ_to=L
        )

        posx = 250
        posy = 250

        image = Image.open(
            DATA_PATH + "results/parallel_experiment_result.png"
        )
        image = image.resize((500, 300))
        image = ImageTk.PhotoImage(image)
        self.result_images.append(image)
        self.canvas.create_image(posx, posy, image=image)
