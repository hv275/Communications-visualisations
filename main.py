# import our dear libraries
from pages import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
import os

import matplotlib
matplotlib.use("TkAgg")


LARGE_FONT = ("Verdana", 12)


class SignalSandbox(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


app = SignalSandbox()
app.mainloop()
