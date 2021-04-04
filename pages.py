import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from oscillators import *
import numpy as np
matplotlib.use("TkAgg")
LARGE_FONT = ("Verdana",12)


class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Start Page", font = LARGE_FONT)
        label.pack(pady = 10, padx =10)

        button = ttk.Button(self, text = "Sinusoid Playground", command = lambda: controller.showFrame(SinusoidPlayground))
        button.pack()

        button = ttk.Button(self, text = "Fourier Transform a File", command = lambda:controller.showFrame(TrackTransform))
        button.pack()

class SinusoidPlayground(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Sinusoid Toolbox")
        label.pack(pady = 10, padx = 10)

        returnButton = ttk.Button(self, text = "Return home", command = lambda: controller.showFrame(StartPage))
        returnButton.pack()
        #todo fix entry box to show where I want it
        freqEntry = tk.Entry(self)
        freqEntry.pack()

        plotSinusoid = ttk.Button(self,text = "Plot a sin wave", command = lambda: self.plotWave(int(freqEntry.get()),1))
        plotSinusoid.pack()

        addSinusoid = ttk.Button(self,text = "Superpose a sin wave", command = lambda: self.superposeWave(int(freqEntry.get())))
        addSinusoid.pack()

        showFFT = ttk.Button(self, text = "Show Fourier Transform of a Signal", command = lambda: self.showFourierTransform())
        showFFT.pack()

        #do so this figure is generated live
        self.fig = Figure(figsize=(5,5),dpi = 100)
        self.a = self.fig.add_subplot(211)
        self.a.title.set_text("Signal")
        self.fft = self.fig.add_subplot(212)
        self.fft.title.set_text("Frequencies")
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig,self)
        self.canvas._tkcanvas.pack(side = tk.TOP,fill = tk.BOTH,expand = True)
        self.toolbar = NavigationToolbar2Tk(self.canvas,self)
        self.toolbar.update()

        #set up a cache
        self.cache = {"times":[],"wave":[],"dur":1}
        


    def plotWave(self,freq,end):
        self.a.cla()
        self.cache["times"],self.cache["wave"] = sinosc(freq,end)
        self.cache["dur"] = end
        self.a.plot(self.cache["times"],self.cache["wave"])
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH,expand = True)
        self.canvas.draw()

    #todo, live nyquist frequency modification
    #fft works for now
    def superposeWave(self,freq):
        self.a.cla()
        _,vals = sinosc(freq,self.cache["dur"])
        self.cache["wave"]+=vals
        self.a.plot(self.cache["times"],self.cache["wave"])
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH,expand = True)
        self.canvas.draw()
        
    def showFourierTransform(self):
        self.fft.cla()
        fftvals = np.fft.fft(self.cache["wave"])
        N = fftvals.size
        fs = 1/(self.cache["dur"]/len(self.cache["wave"]))
        bins = np.arange(0,N)*fs/N
        #I am essentially throwing away the second half of the transform, as it is a repeat
        fftvals,_ = np.array_split(np.trim_zeros(fftvals,"b"),2)
        bins,_ = np.array_split(np.trim_zeros(bins,"b"),2)
        self.fft.plot(bins,np.abs(fftvals))
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH,expand = True)
        self.canvas.draw()



class TrackTransform(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Cheeky Fourier Transforms")
        label.pack(pady = 10, padx = 10)
        returnButton = ttk.Button(self, text = "Return home", command = lambda: controller.showFrame(StartPage))
        returnButton.pack()




#kinda sample code, not doing much atm
class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "Graph Page", font = LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self,text = "Back to home", command = lambda: controller.show_frame(StartPage))

