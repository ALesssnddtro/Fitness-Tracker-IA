from tkinter import *
from tkinter import ttk

LARGEFONT = ("Verdana", 35)


class tkinterApp(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.geometry("650x650")
        self.title("Fitness Tracker")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Main, Page1, Page2):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Main)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Main(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        button1 = ttk.Button(self, text="Main", command=lambda: controller.show_frame(Main), width=10)
        button1.grid(row=0, column=0)

        button2 = ttk.Button(self, text="Page 1", command=lambda: controller.show_frame(Page1), width=10)
        button2.grid(row=0, column=1)

        button3 = ttk.Button(self, text="Page 2", command=lambda: controller.show_frame(Page2), width=10)
        button3.grid(row=0, column=2)


# second window frame page1
class Page1(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        button1 = ttk.Button(self, text="Main", command=lambda: controller.show_frame(Main), width=10)
        button1.grid(row=0, column=0)

        button2 = ttk.Button(self, text="Page 1", command=lambda: controller.show_frame(Page1), width=10)
        button2.grid(row=0, column=1)

        button3 = ttk.Button(self, text="Page 2", command=lambda: controller.show_frame(Page2), width=10)
        button3.grid(row=0, column=2)


# third window frame page2
class Page2(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        button1 = ttk.Button(self, text="Main", command=lambda: controller.show_frame(Main), width=10)
        button1.grid(row=0, column=0)

        button2 = ttk.Button(self, text="Page 1", command=lambda: controller.show_frame(Page1), width=10)
        button2.grid(row=0, column=1)

        button3 = ttk.Button(self, text="Page 2", command=lambda: controller.show_frame(Page2), width=10)
        button3.grid(row=0, column=2)


# Driver Code
app = tkinterApp()
app.mainloop()

