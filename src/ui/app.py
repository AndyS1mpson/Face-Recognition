from tkinter import Tk, ttk

from ui.frames import ExperimentFrame, ResearchFrame


class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Face Recognition")
        self.attributes("-zoomed", True)

        self.notebook = ttk.Notebook(self)

        self.ex_tab = ExperimentFrame(self.notebook)
        self.research_tab = ResearchFrame(self.notebook)

        self.notebook.add(self.ex_tab, text="Эксперимент")
        self.notebook.add(self.research_tab, text="Исследование")
        self.notebook.pack(expand=1, fill="both")
