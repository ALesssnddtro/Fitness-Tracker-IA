from tkinter import *
from tkinter import ttk

LARGEFONT = ("Verdana", 35)


class tkinterApp(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.geometry("540x300")
        self.resizable(width=False, height=False)
        self.title("Fitness Tracker")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Profile, DailyActivity, AddWorkout, Calender, Settings):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Profile)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

def toolbar(self, controller):
    
    Bwidth = 8
    Fsize = 11
    button_plus = Button(self, text='Calender', command=lambda: controller.show_frame(Calender), bg="gray70",
                     bd=3, padx=11, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    button_plus.grid(row=10, column=0, sticky=S)

    
    button_plus = Button(self, text='DailyActivity', command=lambda: controller.show_frame(DailyActivity), bg="gray70",
                     bd=3, padx=11, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    button_plus.grid(row=10, column=1, sticky=S)

    
    button_plus = Button(self, text='+', command=lambda: controller.show_frame(AddWorkout), bg="gray70",
                     bd=3, padx=11, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    button_plus.grid(row=10, column=2, sticky=S)


    button_plus = Button(self, text='Profile', command=lambda: controller.show_frame(Profile), bg="gray70",
                     bd=3, padx=11, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    button_plus.grid(row=10, column=3, sticky=S)


    button_plus = Button(self, text='Settings', command=lambda: controller.show_frame(Settings), bg="gray70",
                     bd=3, padx=11, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    button_plus.grid(row=10, column=4, sticky=S)
    

class Profile(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        toolbar(self, controller)
        
        

# second window frame page1
class DailyActivity(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        toolbar(self, controller)
        add_btn = Button(self, text='Add Session', width=12)
        add_btn.grid(row=4, column=0)

        remove_btn = Button(self, text='Remove Session', width=12)
        remove_btn.grid(row=4, column=1)

        update_btn = Button(self, text='Update Session', width=12)
        update_btn.grid(row=4, column=2)

        clear_btn = Button(self, text='Clear Input', width=12)
        clear_btn.grid(row=4, column=3)


# third window frame page2
class AddWorkout(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        toolbar(self, controller)



class Calender(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        toolbar(self, controller)

class Settings(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        toolbar(self, controller)


# Driver Code
app = tkinterApp()
app.mainloop()

