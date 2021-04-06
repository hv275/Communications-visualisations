import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import scipy.io.wavfile as wv
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

        button = ttk.Button(self, text = "Modulation Playground", command = lambda:controller.showFrame(ModulationPage))
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
        freqLabel = tk.Label(self,text = "Frequency")
        freqLabel.pack()
        freqEntry.pack()

        magEntry = tk.Entry(self)
        magEntry.insert(0,"1")
        magLabel = tk.Label(self,text = "Magnitude")
        magLabel.pack()
        magEntry.pack()

        plotSinusoid = ttk.Button(self,text = "Plot a sin wave", command = lambda: self.plotWave(float(freqEntry.get()),1,float(magEntry.get())))
        plotSinusoid.pack()

        addSinusoid = ttk.Button(self,text = "Superpose a sin wave", command = lambda: self.superposeWave(float(freqEntry.get()),float(magEntry.get())))
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
        


    def plotWave(self,freq,end,mag):
        self.a.cla()
        self.cache["times"],self.cache["wave"] = sinosc(freq,end,mag)
        self.cache["dur"] = end
        self.a.plot(self.cache["times"],self.cache["wave"])
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH,expand = True)
        self.canvas.draw()

    #todo, live nyquist frequency modification
    #fft works for now
    def superposeWave(self,freq,mag):
        self.a.cla()
        _,vals = sinosc(freq,self.cache["dur"],mag)
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
        choiceButton = ttk.Button(self,text = "Choose file to transform", command = self.openFile)
        choiceButton.pack()

    
    def openFile(self):
        self.file = tk.filedialog.askopenfilename(filetypes=(("Wav files",".wav"),("All files","*.*")))
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

        fs, signal = wv.read(self.file)
        #just using one channel as I cba converting stereo to mono without it sounding like ass
        signal = signal[:,0]
        t = [i/fs for i in range(signal.size)]
        self.a.plot(t,signal)

        fftvals = np.fft.fft(signal)
        N = fftvals.size
        bins = np.arange(0,N)*fs/N
        #I am essentially throwing away the second half of the transform, as it is a repeat
        #fftvals,_ = np.array_split(np.trim_zeros(fftvals,"b"),2)
        #bins,_ = np.array_split(np.trim_zeros(bins,"b"),2)
        self.fft.plot(bins,np.abs(fftvals))
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH,expand = True)
        self.canvas.draw()



class ModulationPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Examples of Modulation")
        label.pack(pady = 10, padx = 10)
        lable = tk.Label(self,text = "Note, currently only planning to show analogue modulation techniques and carrier is set in code")
        returnButton = ttk.Button(self, text = "Return home", command = lambda: controller.showFrame(StartPage))
        returnButton.pack()

        signalButton = ttk.Button(self, text="Choose signal to modulate", command = lambda: self.pickFile())
        signalButton.pack()

        MODULATION = ["AM","AM","DSB-SC","SSB-SC","FM"]
        modVar = tk.StringVar(self)
        modVar.set("AM")
        modSelect = ttk.OptionMenu(self,modVar,*MODULATION)
        modSelect.pack()
        modulateButton = ttk.Button(self,text = "Modulate", command = lambda: self.modulate(modVar.get()))
        modulateButton.pack()
        fftButton = ttk.Button(self,text = "Show Fourier Transform", command = lambda: self.showFT())
        fftButton.pack()


        #currently creating graphs in frames but may look into doing it in functions to have more flexibility or smth
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



    def pickFile(self):
        self.file = tk.filedialog.askopenfilename(filetypes=(("Wav files",".wav"),("All files","*.*")))
        self.fs, signal = wv.read(self.file)
        #just using one channel as I cba converting stereo to mono without it sounding like ass
        self.signal = signal[:,0]
        print(self.signal.size)
        self.t = [i/self.fs for i in range(self.signal.size)]
        self.a.plot(self.t,self.signal)
        self.canvas.draw()

    def showFT(self):
                    #Note to self, I am not 100% on whether the fft works exactly like intended but oh well
        fftvals = np.fft.fft(self.signal)
        N = fftvals.size
        bins = np.arange(0,N)*self.fs/N
        #I am essentially throwing away the second half of the transform, as it is a repeat
        #fftvals,_ = np.array_split(np.trim_zeros(fftvals,"b"),2)
        #bins,_ = np.array_split(np.trim_zeros(bins,"b"),2)
        self.fft.plot(bins,np.abs(fftvals))
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH,expand = True)
        self.canvas.draw()

    def modulate(self,modType):
        print(modType)
        if modType == "AM":
            _, carrier = sinosc(1e6,self.t[-1]+1/self.fs,1,self.fs)
            self.signal = (self.signal + 1e3)*carrier
            self.a.plot(self.t,self.signal)
            self.canvas.draw()

            


        else:
            print("Feature not yet implemented")
            
        
        
            
            






        






#kinda sample code, not doing much atm
class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "Graph Page", font = LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self,text = "Back to home", command = lambda: controller.show_frame(StartPage))

        


