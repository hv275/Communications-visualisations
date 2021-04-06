# import our dear libraries

from pages import *
import tkinter as tk
import numpy as np
import os

#honestly, it would have been easier to write a web app for this but I cba dealing with html and flask
#like plotly would have been greate but that is not the point
#


LARGE_FONT = ("Verdana", 12)


class SignalSandbox(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for i in (StartPage,SinusoidPlayground,TrackTransform,ModulationPage):
            frame = i(container,self)
            self.frames[i] = frame
            frame.grid(row = 0, column=0,sticky = "nsew")

        self.showFrame(StartPage)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


app = SignalSandbox()
app.mainloop()
