from tkinter import (RIGHT, Y, Button, Entry, Label, OptionMenu, Scrollbar, StringVar, Tk,
                     ttk, Frame, Canvas, VERTICAL, HORIZONTAL)

from ui.frames import ExperimentFrame


class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = "Face Recognition"
        self.attributes('-zoomed', True)

        self.notebook = ttk.Notebook(self)

        self.research_tab = Frame(self.notebook)
        self.ex_tab = ExperimentFrame(self.notebook)


        self.notebook.add(self.ex_tab, text="Эксперимент")
        self.notebook.add(self.research_tab, text="Исследование")
        self.notebook.pack(expand=1, fill="both")
