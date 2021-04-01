import tkinter as tk
LARGE_FONT = ("Verdana",12)


class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Start Page", font = LARGE_FONT)
        label.pack(pady = 10, padx =10)

        button = tk.Button(self, text = "Visit Page 1", command = lambda: print("Hello World"))
        button.pack()




class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "Graph Page", font = LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self,text = "Back to home", command = lambda: controller.show_frame(StartPage))