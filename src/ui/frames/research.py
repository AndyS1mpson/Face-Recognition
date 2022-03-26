from tkinter import (BOTH, BOTTOM, HORIZONTAL, NW, TOP, Button, Canvas, Frame,
                     Label, N, OptionMenu, Scrollbar, StringVar, W, X)

from PIL import Image, ImageTk

from core.config.config import ALL_METHODS, DATA_PATH
from core.research import research


class ResearchFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Метод извлечения признаков
        self.method_label = Label(self, text="Параметр")
        self.method_label.pack(side=TOP, padx=10, pady=7, anchor=NW)

        self.method = StringVar()
        self.method.set(ALL_METHODS[1])

        self.method_drop = OptionMenu(self, self.method, *ALL_METHODS)
        self.method_drop.configure(width=10)
        self.method_drop.pack(side=TOP, padx=10, pady=7, anchor=NW)

        # Список классифицируемых изображений
        self.result_images = []

        # Запуск исследования

        self.run_but = Button(
            self, text="Запустить", command=lambda: self.show_result()
        )
        self.run_but.pack(side=TOP, padx=10, pady=7, anchor=NW)

        self.canvas = Canvas(self, width=1500, height=800)

        self.scroll_x = Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)
        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.canvas.pack(fill=BOTH, expand=True)

        self.columnconfigure(0, weight=1)
        self.canvas.config(
            xscrollcommand=self.scroll_x.set, scrollregion=self.canvas.bbox("all")
        )

        self.canvas.create_window((0, 0), window=self, anchor=N + W)

    def show_result(self):
        global image
        best_scores, _, _ = research("ORL", self.method.get())

        posx = 250
        posy = 250

        for index, _ in enumerate(best_scores):

            image = Image.open(DATA_PATH + f"results/result_{index}.png")
            image = image.resize((350, 350))
            image = ImageTk.PhotoImage(image)
            self.result_images.append(image)
            self.canvas.create_image(posx, posy, image=image)

            posx += 360
