import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from oscillators import *
matplotlib.use("TkAgg")
LARGE_FONT = ("Verdana",12)


class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Start Page", font = LARGE_FONT)
        label.pack(pady = 10, padx =10)

        button = ttk.Button(self, text = "Sinusoid Playground", command = lambda: controller.showFrame(SinusoidPlayground))
        button.pack()

class SinusoidPlayground(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Sinusoid Toolbox")
        label.pack(pady = 10, padx = 10)

        returnButton = ttk.Button(self, text = "Return home", command = lambda: controller.showFrame(StartPage))
        returnButton.pack()
        #todo fix entry box to show where I want it
        freqEntry = tk.Entry()
        freqEntry.pack()

        plotSinusoid = ttk.Button(self,text = "Plot a sin wave", command = lambda: self.plotWave(int(freqEntry.get()),1))
        plotSinusoid.pack()

        #todo, create an ability to stack waves
        self.fig = Figure(figsize=(5,5),dpi = 100)
        self.a = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig,self)
        self.canvas._tkcanvas.pack(side = tk.TOP,fill = tk.BOTH,expand = True)
        self.toolbar = NavigationToolbar2Tk(self.canvas,self)
        self.toolbar.update()
        


    def plotWave(self,freq,end):
        self.a.cla()
        t,vals = sinosc(freq,end)
        self.a.plot(t,vals)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH,expand = True)
        self.canvas.draw()






class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "Graph Page", font = LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self,text = "Back to home", command = lambda: controller.show_frame(StartPage))