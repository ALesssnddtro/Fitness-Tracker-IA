import sqlite3
from datetime import datetime
from datetime import timedelta
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview

from tkcalendar import *

Bwidth = 12
Fsize = 11
conn = sqlite3.connect('library.db')
c = conn.cursor()


def reminder_check():
    Notif = False

    CurrentDate = datetime.now()

    for row in c.execute('SELECT * FROM Sessions'):
        Duration = row[4]
        CurrentDate = CurrentDate.strftime("%Y/%m/%d %I:%M %p")
        CurrentDate = datetime.strptime(CurrentDate, "%Y/%m/%d %H:%M %p")

        ExpectedDateMin = row[2] + " " + row[3]
        ExpectedDateMin = datetime.strptime(ExpectedDateMin, "%Y/%m/%d %H:%M")
        ExpectedDateMax = ExpectedDateMin + timedelta(minutes=Duration)

        if CurrentDate > ExpectedDateMin and CurrentDate < ExpectedDateMax:
            Notif = True

    return Notif


def first_start_up_check():
    FirstStartUp = False

    c.execute("SELECT * FROM User")

    data = c.fetchall()

    if len(data) == 0:
        FirstStartUp = True

    return FirstStartUp


class tkinterApp(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.geometry("600x550")
        self.resizable(width=False, height=False)
        self.title("Fitness Tracker")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (
                NewUser, Profile, DailyActivity_Day, DailyActivity_Week, DailyActivity_Month, AddWorkout,
                CalenderSearch,
                Settings, ReminderPopUp, WorkoutCalendar,
                SessionScreenInfo, SpecificExerciseDetails, AddRoutine, Routine_edit_days, SessionScreenEdit,
                AddExercise, UserScreenEdit, ExerciseListEdit):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        c.execute("SELECT Reminders FROM User")
        reminders_on = c.fetchone()[0]

        if first_start_up_check():
            self.show_frame(NewUser)
        else:
            if (reminders_on == 1): #and reminder_check():
                self.show_frame(ReminderPopUp)
            else:
                self.show_frame(Profile)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

    def find_page(self, page_class):
        return self.frames[page_class]


def toolbar(self, controller):
    button_plus = Button(self, text='Calender', command=lambda: controller.show_frame(WorkoutCalendar), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    button_plus.place(relx=0.1, rely=1, anchor=S)

    button_plus = Button(self, text='Activity', command=lambda: controller.show_frame(DailyActivity_Day), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    button_plus.place(relx=0.3, rely=1, anchor=S)

    button_plus = Button(self, text='+', command=lambda: controller.show_frame(AddWorkout), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    button_plus.place(relx=0.5, rely=1, anchor=S)

    button_plus = Button(self, text='Profile', command=lambda: controller.show_frame(Profile), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    button_plus.place(relx=0.7, rely=1, anchor=S)

    button_plus = Button(self, text='Settings', command=lambda: controller.show_frame(Settings), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    button_plus.place(relx=0.9, rely=1, anchor=S)


class NewUser(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        lb_first_name = Label(self, text="First name")
        en_first_name = Entry(self)
        lb_first_name.place(relx=0.43, rely=0.15, anchor=E)
        en_first_name.place(relx=0.65, rely=0.15, anchor=E)

        lb_last_name = Label(self, text="Last name")
        en_last_name = Entry(self)
        lb_last_name.place(relx=0.43, rely=0.25, anchor=E)
        en_last_name.place(relx=0.65, rely=0.25, anchor=E)

        lb_DoB = Label(self, text="DoB")
        en_DoB = Entry(self)
        lb_DoB.place(relx=0.43, rely=0.35, anchor=E)
        en_DoB.place(relx=0.65, rely=0.35, anchor=E)

        lb_weight = Label(self, text="Weight")
        en_weight = Entry(self)
        lb_weight.place(relx=0.43, rely=0.45, anchor=E)
        en_weight.place(relx=0.65, rely=0.45, anchor=E)

        lb_target_weight = Label(self, text="Target Weight")
        en_target_weight = Entry(self)
        lb_target_weight.place(relx=0.43, rely=0.55, anchor=E)
        en_target_weight.place(relx=0.65, rely=0.55, anchor=E)

        lb_height = Label(self, text="Height")
        en_height = Entry(self)
        lb_height.place(relx=0.43, rely=0.65, anchor=E)
        en_height.place(relx=0.65, rely=0.65, anchor=E)

        lb_gender = Label(self, text="Gender")
        en_gender = Entry(self)
        lb_gender.place(relx=0.43, rely=0.75, anchor=E)
        en_gender.place(relx=0.65, rely=0.75, anchor=E)

        def create_user():
            c.execute("INSERT INTO User VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (1, en_last_name.get(), en_first_name.get(),
                                                                           en_DoB.get(), en_weight.get(),
                                                                           en_target_weight.get(), en_height.get(),
                                                                           en_gender.get()))
            conn.commit()
            controller.show_frame(Profile)

        create_btn = Button(self, text='Create User', width=3, command=create_user)
        create_btn.place(relx=0.5, rely=0.85, anchor=N)


def calc_bmi():
    c.execute('SELECT Weight, Height FROM User')
    data = c.fetchall()[0]
    meters_height = float(data[1]) / 100
    bmi = data[0] / meters_height * meters_height

    return bmi


class Profile(Frame):
    def on_show_frame(self, event):
        c.execute('SELECT * FROM User')
        self.User_Data = c.fetchall()[0]

        self.var_name.set(self.User_Data[2] + " " + self.User_Data[1])
        self.var_weight.set(str(self.User_Data[4]) + " Kg")
        self.var_target_weight.set(str(self.User_Data[5]) + " Kg")
        self.var_bmi.set(calc_bmi())

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)  # when frame is loaded
        self.configure(bg="#B3B3B3")

        c.execute('SELECT * FROM User')
        self.User_Data = c.fetchall()[0]
        if len(self.User_Data) == 0:
            self.User_Data = [("Last Name", "First Name", "DoB", "Weight", "Target Weight", "Height", "Gender")]

        self.var_name = StringVar()
        self.var_bmi = IntVar()
        self.var_weight = StringVar()
        self.var_target_weight = StringVar()
        print(self.User_Data)
        self.var_name.set(self.User_Data[2] + " " + self.User_Data[1])
        self.var_weight.set(str(self.User_Data[4]) + " Kg")
        self.var_target_weight.set(str(self.User_Data[5]) + " Kg")
        self.var_bmi.set(calc_bmi())

        name_label = Label(self, textvariable=self.var_name)
        name_label.place(relx=0.5, rely=0.5, anchor=N)

        lb_bmi = Label(self, text="BMI")
        en_bmi = Entry(self, textvariable=self.var_bmi, state="disabled")

        btn_bmi_info = Button(self, text="i", command=bmi_info, font="italic")

        lb_weight = Label(self, text="Weight")
        en_weight = Entry(self, textvariable=self.var_weight, state="disabled")

        lb_target_weight = Label(self, text="Target Weight")
        en_target_weight = Entry(self, textvariable=self.var_target_weight, state="disabled")

        lb_bmi.place(relx=0.2, rely=0.65, anchor=S)
        en_bmi.place(relx=0.2, rely=0.70, anchor=S)

        lb_weight.place(relx=0.5, rely=0.65, anchor=S)
        en_weight.place(relx=0.5, rely=0.70, anchor=S)

        lb_target_weight.place(relx=0.8, rely=0.65, anchor=S)
        en_target_weight.place(relx=0.8, rely=0.70, anchor=S)

        btn_bmi_info.place(relx=0.25, rely=0.65, anchor=S)

        toolbar(self, controller)


def bmi_info():
    pop_up = Toplevel()
    pop_up.geometry("200x140")
    pop_up.title("data")
    btn_button = Button(pop_up, text="close", command=lambda: pop_up.destroy())

    lb_info_title = Label(pop_up, text="BMI Categories:")
    lb_info_Un = Label(pop_up, text="Underweight = <18.5")
    lb_info_No = Label(pop_up, text="Normal weight = 18.5–24.9")
    lb_info_Ov = Label(pop_up, text="Overweight = 25–29.9")
    lb_info_Ob = Label(pop_up, text="Obesity = BMI of 30 or greater")
    lb_info_title.pack()
    lb_info_Un.pack()
    lb_info_No.pack()
    lb_info_Ov.pack()
    lb_info_Ob.pack()
    btn_button.pack()


class activity:
    @staticmethod
    def day(index):
        CurrentDay = datetime.now().date() + timedelta(days=index)

        return '''SELECT SUM(Exercises.CaloriesBurntPerRep * SessionDetails.Reps * SessionDetails.Sets) AS TotalCalPerSession, Sessions.Duration 
                FROM Sessions INNER JOIN SessionDetails ON Sessions.SessionID = SessionDetails.SessionID 
                INNER JOIN Exercises ON SessionDetails.ExerciseID = Exercises.ExerciseID WHERE StartDate = ''' + "'" + str(
            CurrentDay).replace('-', '/') + "'"

    @staticmethod
    def week(index):
        CurrentDay = datetime.now().date() + timedelta(weeks=index)

        date_start_of_week = CurrentDay - timedelta(days=CurrentDay.weekday())
        date_end_of_week = date_start_of_week + timedelta(days=6)

        return '''SELECT SUM(Exercises.CaloriesBurntPerRep * SessionDetails.Reps * SessionDetails.Sets) AS TotalCalPerSession, SUM(Sessions.Duration) 
                FROM Sessions INNER JOIN SessionDetails ON Sessions.SessionID = SessionDetails.SessionID 
                INNER JOIN Exercises ON SessionDetails.ExerciseID = Exercises.ExerciseID WHERE StartDate BETWEEN ''' + "'" + str(
            date_start_of_week).replace('-', '/') + "' AND " + "'" + str(date_end_of_week).replace('-', '/') + "'"

    @staticmethod
    def month(index):
        CurrentDay = datetime.now().date() + timedelta(weeks=index * 5)

        next_month = CurrentDay.replace(day=28) + timedelta(days=4)

        date_end_of_month = next_month - timedelta(days=next_month.day)
        date_start_of_month = date_end_of_month.replace(day=1)

        return '''SELECT SUM(Exercises.CaloriesBurntPerRep * SessionDetails.Reps * SessionDetails.Sets) AS TotalCalPerSession, SUM(Sessions.Duration) 
                FROM Sessions INNER JOIN SessionDetails ON Sessions.SessionID = SessionDetails.SessionID 
                INNER JOIN Exercises ON SessionDetails.ExerciseID = Exercises.ExerciseID WHERE StartDate BETWEEN ''' + "'" + str(
            date_start_of_month).replace('-', '/') + "' AND " + "'" + str(date_end_of_month).replace('-', '/') + "'"


class DailyActivity_Day(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        var_calories_burnt = IntVar()
        var_time_spent = IntVar()
        var_show_date = StringVar()
        var_index = IntVar(0)

        def left_nav():
            var_index.set(var_index.get() - 1)
            loaddata()

        def right_nav():
            var_index.set(var_index.get() + 1)
            loaddata()

        def loaddata():
            day_query = activity.day(var_index.get())
            c.execute(day_query)
            data = c.fetchall()[0]
            var_show_date.set(str(datetime.now().date() + timedelta(days=var_index.get())))
            var_calories_burnt.set(data[0])
            var_time_spent.set(data[1])
            print(data)

        btn_left = Button(self, command=left_nav, text='<')
        btn_left.place(relx=0.3, rely=0.15, anchor=N)

        btn_left = Button(self, command=right_nav, text='>')
        btn_left.place(relx=0.7, rely=0.15, anchor=N)

        lb_exercise_name = Label(self, text='Daily')
        lb_exercise_name.place(relx=0.5, rely=0.1, anchor=N)

        en_exercise_name = Entry(self, textvariable=var_show_date, state="disabled", width=30)
        en_exercise_name.place(relx=0.5, rely=0.15, anchor=N)

        lb_exercise_name = Label(self, text="Total Calories Burnt")
        lb_exercise_name.place(relx=0.1, rely=0.30, anchor=W)

        en_exercise_name = Entry(self, textvariable=var_calories_burnt, state="disabled")
        en_exercise_name.place(relx=0.4, rely=0.30, anchor=W)

        lb_exercise_name = Label(self, text="Total Time Spent Exercising")
        lb_exercise_name.place(relx=0.1, rely=0.40, anchor=W)

        en_exercise_name = Entry(self, textvariable=var_time_spent, state="disabled")
        en_exercise_name.place(relx=0.4, rely=0.40, anchor=W)

        btn_day = Button(self, text='Daily', command=lambda: controller.show_frame(DailyActivity_Day), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=12)
        btn_day.place(relx=0.3, rely=0.7, anchor=N)

        btn_week = Button(self, text='Weekly', command=lambda: controller.show_frame(DailyActivity_Week), bg="gray70",
                          bd=3, pady=5, font=("Helvetica", Fsize), width=12)
        btn_week.place(relx=0.5, rely=0.7, anchor=N)

        btn_month = Button(self, text='Monthly', command=lambda: controller.show_frame(DailyActivity_Month),
                           bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=12)
        btn_month.place(relx=0.7, rely=0.7, anchor=N)

        toolbar(self, controller)


class DailyActivity_Week(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        var_calories_burnt = IntVar()
        var_time_spent = IntVar()
        var_show_date = StringVar()
        var_index = IntVar(0)

        def left_nav():
            var_index.set(var_index.get() - 1)
            update_entries()

        def right_nav():
            var_index.set(var_index.get() + 1)
            update_entries()

        def update_entries():
            CurrentDay = datetime.now().date() + timedelta(weeks=var_index.get())

            date_start_of_week = CurrentDay - timedelta(days=CurrentDay.weekday())
            date_end_of_week = date_start_of_week + timedelta(days=6)

            week_query = activity.week(var_index.get())
            c.execute(week_query)
            data = c.fetchall()[0]
            var_show_date.set(str(date_start_of_week) + " to " + str(date_end_of_week))
            var_calories_burnt.set(data[0])
            var_time_spent.set(data[1])
            print(data)

        btn_left = Button(self, command=left_nav, text='<')
        btn_left.place(relx=0.3, rely=0.15, anchor=N)

        btn_left = Button(self, command=right_nav, text='>')
        btn_left.place(relx=0.7, rely=0.15, anchor=N)

        lb_exercise_name = Label(self, text='Weekly')
        lb_exercise_name.place(relx=0.5, rely=0.1, anchor=N)

        en_exercise_name = Entry(self, textvariable=var_show_date, state="disabled", width=30)
        en_exercise_name.place(relx=0.5, rely=0.15, anchor=N)

        lb_exercise_name = Label(self, text="Total Calories Burnt")
        lb_exercise_name.place(relx=0.1, rely=0.30, anchor=W)

        en_exercise_name = Entry(self, textvariable=var_calories_burnt, state="disabled")
        en_exercise_name.place(relx=0.4, rely=0.30, anchor=W)

        lb_exercise_name = Label(self, text="Total Time Spent Exercising")
        lb_exercise_name.place(relx=0.1, rely=0.40, anchor=W)

        en_exercise_name = Entry(self, textvariable=var_time_spent, state="disabled")
        en_exercise_name.place(relx=0.4, rely=0.40, anchor=W)

        btn_day = Button(self, text='Daily', command=lambda: controller.show_frame(DailyActivity_Day), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=12)
        btn_day.place(relx=0.3, rely=0.7, anchor=N)

        btn_week = Button(self, text='Weekly', command=lambda: controller.show_frame(DailyActivity_Week), bg="gray70",
                          bd=3, pady=5, font=("Helvetica", Fsize), width=12)
        btn_week.place(relx=0.5, rely=0.7, anchor=N)

        btn_month = Button(self, text='Monthly', command=lambda: controller.show_frame(DailyActivity_Month),
                           bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=12)
        btn_month.place(relx=0.7, rely=0.7, anchor=N)

        toolbar(self, controller)


class DailyActivity_Month(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        var_calories_burnt = IntVar()
        var_time_spent = IntVar()
        var_show_date = StringVar()
        var_index = IntVar(0)

        def left_nav():
            var_index.set(var_index.get() - 1)
            update_entries()

        def right_nav():
            var_index.set(var_index.get() + 1)
            update_entries()

        def update_entries():
            CurrentDay = datetime.now().date() + timedelta(weeks=var_index.get() * 5)

            next_month = CurrentDay.replace(day=28) + timedelta(days=4)

            date_end_of_month = next_month - timedelta(days=next_month.day)
            date_start_of_month = date_end_of_month.replace(day=1)

            month_query = activity.month(var_index.get())
            c.execute(month_query)
            data = c.fetchall()[0]
            var_show_date.set(str(date_start_of_month) + " to " + str(date_end_of_month))
            var_calories_burnt.set(data[0])
            var_time_spent.set(data[1])

        btn_left = Button(self, command=left_nav, text='<')
        btn_left.place(relx=0.3, rely=0.15, anchor=N)

        btn_left = Button(self, command=right_nav, text='>')
        btn_left.place(relx=0.7, rely=0.15, anchor=N)

        lb_exercise_name = Label(self, text='Monthly')
        lb_exercise_name.place(relx=0.5, rely=0.1, anchor=N)

        en_exercise_name = Entry(self, textvariable=var_show_date, state="disabled", width=30)
        en_exercise_name.place(relx=0.5, rely=0.15, anchor=N)

        lb_exercise_name = Label(self, text="Total Calories Burnt")
        lb_exercise_name.place(relx=0.1, rely=0.30, anchor=W)

        en_exercise_name = Entry(self, textvariable=var_calories_burnt, state="disabled")
        en_exercise_name.place(relx=0.4, rely=0.30, anchor=W)

        lb_exercise_name = Label(self, text="Total Time Spent Exercising")
        lb_exercise_name.place(relx=0.1, rely=0.40, anchor=W)

        en_exercise_name = Entry(self, textvariable=var_time_spent, state="disabled")
        en_exercise_name.place(relx=0.4, rely=0.40, anchor=W)

        btn_day = Button(self, text='Daily', command=lambda: controller.show_frame(DailyActivity_Day), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=12)
        btn_day.place(relx=0.3, rely=0.7, anchor=N)

        btn_week = Button(self, text='Weekly', command=lambda: controller.show_frame(DailyActivity_Week), bg="gray70",
                          bd=3, pady=5, font=("Helvetica", Fsize), width=12)
        btn_week.place(relx=0.5, rely=0.7, anchor=N)

        btn_month = Button(self, text='Monthly', command=lambda: controller.show_frame(DailyActivity_Month),
                           bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=12)
        btn_month.place(relx=0.7, rely=0.7, anchor=N)

        toolbar(self, controller)


class AddRoutine(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        var_date_start = StringVar()
        var_time_start = StringVar()
        var_session_duration = IntVar()
        var_exercise_daily = IntVar()

        var_date_start.set("yyyy/mm/dd")
        var_time_start.set("hh:mm")

        Workout_Monday = IntVar()
        Workout_Tuesday = IntVar()
        Workout_Wednesday = IntVar()
        Workout_Thursday = IntVar()
        Workout_Friday = IntVar()
        Workout_Saturday = IntVar()
        Workout_Sunday = IntVar()

        routine_goal = IntVar()
        routine_intensity = IntVar()

        # pull day [0][i]        #leg day [1][i]         #push day [2][i]
        Build_muscles_list = (
            ["Barbell Row", "Hammer Curl", "DB Shrugs", "Bicep Curls", "Dumbbell Rows", "Inclined Curls"],
            ["Hip Thrusts", "Step-Ups", "Lunges", "Squats", "Deadlifts", "Romanian deadlift"],
            ["Bench Press", "Front Squats", "Overhead Press", "Tricep Extension", "DB Lateral raises", "Seated press"])
        Lose_weight_list = ([], [])

        lb_rest_days = Label(self, text="Routine Goal")
        lb_rest_days.place(relx=0.5, rely=0.42, anchor=N)

        R1 = Radiobutton(self, text="Lose weight", variable=routine_goal, value=0)
        R1.place(relx=0.3, rely=0.47, anchor=N)

        R2 = Radiobutton(self, text="Build Muscles", variable=routine_goal, value=1)
        R2.place(relx=0.5, rely=0.47, anchor=N)

        R2 = Radiobutton(self, text="Combination", variable=routine_goal, value=2)
        R2.place(relx=0.7, rely=0.47, anchor=N)

        lb_rest_days = Label(self, text="Workout Intensity")
        lb_rest_days.place(relx=0.5, rely=0.55, anchor=N)

        rb_intensity_high = Radiobutton(self, text="High", variable=routine_intensity, value=12)
        rb_intensity_high.place(relx=0.3, rely=0.6, anchor=N)

        rb_intensity_mid = Radiobutton(self, text="Mid", variable=routine_intensity, value=10)
        rb_intensity_mid.place(relx=0.5, rely=0.6, anchor=N)

        rb_intensity_low = Radiobutton(self, text="Low", variable=routine_intensity, value=8)
        rb_intensity_low.place(relx=0.7, rely=0.6, anchor=N)

        lb_timeStart = Label(self, text="Start Date")
        en_timeStart = Entry(self, textvariable=var_date_start, bd=5)
        lb_timeStart.place(relx=0.38, rely=0.13, anchor=NE)
        en_timeStart.place(relx=0.5, rely=0.13, anchor=N)

        lb_timeStart = Label(self, text="Start Time")
        en_timeStart = Entry(self, textvariable=var_time_start, bd=5)
        lb_timeStart.place(relx=0.38, rely=0.23, anchor=NE)
        en_timeStart.place(relx=0.5, rely=0.23, anchor=N)

        lb_timeStart = Label(self, text="Time per session")
        en_timeStart = Entry(self, textvariable=var_session_duration, bd=5)
        lb_timeStart.place(relx=0.38, rely=0.33, anchor=NE)
        en_timeStart.place(relx=0.5, rely=0.33, anchor=N)

        date_until = 2  # multiple of 7 of days

        def add():

            if (Workout_Monday.get() == 1 and Workout_Tuesday.get() == 1 and Workout_Wednesday.get() == 1
                and Workout_Thursday.get() == 1 and Workout_Friday.get() == 1 and Workout_Saturday.get() == 1
                and Workout_Sunday.get() == 1) or (
                    Workout_Monday.get() == 0 and Workout_Tuesday.get() == 0 and Workout_Wednesday.get() == 0
                    and Workout_Thursday.get() == 0 and Workout_Friday.get() == 0 and Workout_Saturday.get() == 0
                    and Workout_Sunday.get() == 0):
                print("fix ur ticks")
            else:
                day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                rest_days = []
                if Workout_Monday.get() == 1:
                    rest_days.append(day_name[0])

                if Workout_Tuesday.get() == 1:
                    rest_days.append(day_name[1])

                if Workout_Wednesday.get() == 1:
                    rest_days.append(day_name[2])

                if Workout_Thursday.get() == 1:
                    rest_days.append(day_name[3])

                if Workout_Friday.get() == 1:
                    rest_days.append(day_name[4])

                if Workout_Saturday.get() == 1:
                    rest_days.append(day_name[5])

                if Workout_Sunday.get() == 1:
                    rest_days.append(day_name[6])

                current_date = var_date_start.get()
                for x in range(date_until * 7):
                    to_date = datetime.strptime(current_date, "%Y/%m/%d").date()
                    date = to_date + timedelta(days=x)
                    week_day = date.weekday()

                    if day_name[week_day] not in rest_days:
                        c.execute("SELECT SessionID FROM Sessions ORDER BY SessionID DESC LIMIT 1")
                        last_SessionID = c.fetchone()
                        insert_date_array = str(date).split("-")
                        final_date = insert_date_array[0] + "/" + insert_date_array[1] + "/" + insert_date_array[2]

                        c.execute("INSERT INTO Sessions VALUES (?, ?, ?, ?, ?, ?, ?)",
                                  (last_SessionID[0] + 1, 1, final_date, str(var_time_start.get()),
                                   var_session_duration.get(), "Gym", "True"))
                        for y in range(6):
                            c.execute(
                                "SELECT SessionDetailsID FROM SessionDetails ORDER BY SessionDetailsID DESC LIMIT 1")
                            last_SessionDetailsID = c.fetchone()
                            c.execute("INSERT INTO SessionDetails VALUES (?, ?, ?, ?, ?)",
                                      (last_SessionDetailsID[0] + 1, last_SessionID[0] + 1, y, 3, 12))
                        conn.commit()

        btn_day_show = Button(self, text='Workout Routine', bg="gray70",
                              command=lambda: controller.show_frame(AddRoutine),
                              bd=3, pady=2, font=("Helvetica", Fsize), width=13)
        btn_day_show.place(relx=0.4, rely=0.1, anchor=S)

        btn_year_show = Button(self, text='Session', bg="gray70", command=lambda: controller.show_frame(AddWorkout),
                               bd=3, pady=2, font=("Helvetica", Fsize), width=7)
        btn_year_show.place(relx=0.6, rely=0.1, anchor=S)

        btn_year_show = Button(self, text='Clear', bg="gray70",
                               bd=3, pady=2, font=("Helvetica", Fsize), width=7)
        btn_year_show.place(relx=0.4, rely=0.8, anchor=N)

        btn_create_routine = Button(self, text="Create Routine", bg="gray70",
                                    bd=3, pady=2, font=("Helvetica", Fsize), width=12)
        btn_create_routine.place(relx=0.6, rely=0.8, anchor=N)

        lb_rest_days = Label(self, text="Rest Days")
        lb_rest_days.place(relx=0.5, rely=0.68, anchor=N)

        Cwidth = 2
        x_checks = 0.11
        y_checks = 0.755

        C1 = Checkbutton(self, text="M", variable=Workout_Monday, width=Cwidth)
        C2 = Checkbutton(self, text="T", variable=Workout_Tuesday, width=Cwidth)
        C3 = Checkbutton(self, text="W", variable=Workout_Wednesday, width=Cwidth)
        C4 = Checkbutton(self, text="T", variable=Workout_Thursday, width=Cwidth)
        C5 = Checkbutton(self, text="F", variable=Workout_Friday, width=Cwidth)
        C6 = Checkbutton(self, text="S", variable=Workout_Saturday, width=Cwidth)
        C7 = Checkbutton(self, text="S", variable=Workout_Sunday, width=Cwidth)

        C1.place(relx=x_checks, rely=y_checks, anchor=W)
        C2.place(relx=2 * x_checks, rely=y_checks, anchor=W)
        C3.place(relx=3 * x_checks, rely=y_checks, anchor=W)
        C4.place(relx=4 * x_checks, rely=y_checks, anchor=W)
        C5.place(relx=5 * x_checks, rely=y_checks, anchor=W)
        C6.place(relx=6 * x_checks, rely=y_checks, anchor=W)
        C7.place(relx=7 * x_checks, rely=y_checks, anchor=W)

        btn_add = Button(self, text="Add")

        btn_add = Button(self, text="Create")

        toolbar(self, controller)


class Routine_edit_days(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")


class AddWorkout(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        def insert():
            IsPlanned = str(var_is_Planned.get() == 1)

            c.execute("SELECT SessionID FROM Sessions ORDER BY SessionID DESC LIMIT 1")
            last_SessionID = c.fetchone()[0]

            c.execute("INSERT INTO Sessions VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (last_SessionID + 1, 1, var_date_start.get(), var_time_start.get(), var_session_duration.get(),
                       var_session_place.get(), IsPlanned))

            for i in router_tree_view.get_children():
                c.execute('SELECT ExerciseID FROM Exercises WHERE ExerciseName = ?',
                          (router_tree_view.item(i)['values'][0],))
                ex_id = c.fetchone()[0]

                c.execute("SELECT SessionDetailsID FROM SessionDetails ORDER BY SessionDetailsID DESC LIMIT 1")
                last_SessionDetailsID = c.fetchone()[0]

                c.execute("INSERT INTO SessionDetails VALUES (?, ?, ?, ?, ?)",
                          (last_SessionDetailsID + 1, last_SessionID + 1, ex_id, var_exercise_sets.get(),
                           var_exercise_reps.get()))

            conn.commit()

            # reset fields
            var_exercise_name.set("Exercise Name")
            var_date_start.set("yyyy/mm/dd")
            var_time_start.set("hh:mm")
            var_session_duration.set(0)
            var_session_place.set("")
            var_exercise_sets.set(0)
            var_exercise_reps.set(0)

            for i in router_tree_view.get_children():
                router_tree_view.delete(i)

        def add_exercise():
            row = [var_exercise_name.get(), var_exercise_sets.get(), var_exercise_reps.get()]
            # check if exercise exists and sets and reps are valid
            router_tree_view.insert('', 'end', values=row)

        def delete_exercise():
            try:
                selected_item = router_tree_view.selection()
                router_tree_view.delete(selected_item[0])
            except IndexError:
                pass

        var_date_start = StringVar()
        var_time_start = StringVar()
        var_session_duration = IntVar()
        var_session_place = StringVar()
        var_is_Planned = IntVar()

        var_exercise_name = StringVar()
        var_exercise_name.set("Exercise Name")
        var_exercise_sets = IntVar()
        var_exercise_reps = IntVar()

        var_date_start.set("yyyy/mm/dd")
        var_time_start.set("hh:mm")

        lb_timeStart = Label(self, text="Start Date")
        en_timeStart = Entry(self, textvariable=var_date_start, bd=5)
        lb_timeStart.place(relx=0.18, rely=0.13, anchor=NE)
        en_timeStart.place(relx=0.3, rely=0.13, anchor=N)

        lb_timeStart = Label(self, text="Start Time")
        en_timeStart = Entry(self, textvariable=var_time_start, bd=5)
        lb_timeStart.place(relx=0.68, rely=0.13, anchor=NE)
        en_timeStart.place(relx=0.8, rely=0.13, anchor=N)

        lb_timeStart = Label(self, text="Duration")
        en_timeStart = Entry(self, textvariable=var_session_duration, bd=5)
        lb_timeStart.place(relx=0.18, rely=0.23, anchor=NE)
        en_timeStart.place(relx=0.3, rely=0.23, anchor=N)

        lb_timeStart = Label(self, text="Place")
        en_timeStart = Entry(self, textvariable=var_session_place, bd=5)
        lb_timeStart.place(relx=0.68, rely=0.23, anchor=NE)
        en_timeStart.place(relx=0.8, rely=0.23, anchor=N)

        cb_IsPlanned = Checkbutton(self, text="Planned", variable=var_is_Planned)
        cb_IsPlanned.place(relx=0.5, rely=0.3, anchor=N)

        btn_day_show = Button(self, text='Workout Routine', bg="gray70",
                              command=lambda: controller.show_frame(AddRoutine),
                              bd=3, pady=2, font=("Helvetica", Fsize), width=13)
        btn_day_show.place(relx=0.4, rely=0.1, anchor=S)

        btn_year_show = Button(self, text='Session', bg="gray70", command=lambda: controller.show_frame(AddWorkout),
                               bd=3, pady=2, font=("Helvetica", Fsize), width=7)
        btn_year_show.place(relx=0.6, rely=0.1, anchor=S)

        exercise_list = []
        for row in c.execute('SELECT * FROM Exercises'):
            if row[1] not in exercise_list:
                exercise_list.append(row[1])

        op_exType = OptionMenu(self, var_exercise_name, *exercise_list)
        op_exType.config(width=14, font=('Helvetica', Fsize))
        op_exType.place(relx=0.23, rely=0.4, anchor=W)

        lb_timeStart = Label(self, text="Sets")
        en_timeStart = Entry(self, textvariable=var_exercise_sets, bd=5, width=5)
        lb_timeStart.place(relx=0.53, rely=0.4, anchor=W)
        en_timeStart.place(relx=0.58, rely=0.4, anchor=W)

        lb_timeStart = Label(self, text="Reps")
        en_timeStart = Entry(self, textvariable=var_exercise_reps, bd=5, width=5)
        lb_timeStart.place(relx=0.73, rely=0.4, anchor=W)
        en_timeStart.place(relx=0.78, rely=0.4, anchor=W)

        btn_year_show = Button(self, text='Remove Exercise', bg="gray70", command=delete_exercise,
                               bd=3, pady=2, width=14)
        btn_year_show.place(relx=0.3, rely=0.45, anchor=N)

        btn_year_show = Button(self, text='Add Exercise', bg="gray70", command=add_exercise,
                               bd=3, pady=2, width=14)
        btn_year_show.place(relx=0.5, rely=0.45, anchor=N)

        btn_year_show = Button(self, text='Clear Input', bg="gray70",
                               bd=3, pady=2, width=14)
        btn_year_show.place(relx=0.7, rely=0.45, anchor=N)

        col = ['test1', 'test2', 'test3']
        router_tree_view = Treeview(self, columns=col, show="headings")

        router_tree_view.heading('#1', text='Exercise Name')
        router_tree_view.heading('#2', text='Sets')
        router_tree_view.heading('#3', text='Reps')

        router_tree_view.column("#1", width=50)
        router_tree_view.column("#2", width=15)
        router_tree_view.column("#3", width=15)

        router_tree_view.place(relx=0.5, rely=0.52, anchor=N, width=500, height=150)

        btn_create_routine = Button(self, text="Add Session", bg="gray70", command=insert,
                                    bd=3, pady=2, font=("Helvetica", Fsize), width=12)
        btn_create_routine.place(relx=0.5, rely=0.82, anchor=N)

        toolbar(self, controller)


def new_window(rows):
    pop_up = Toplevel()
    pop_up.geometry("750x280")
    pop_up.title("data")
    btn_button = Button(pop_up, text="close", command=lambda: pop_up.destroy())
    btn_button.place(relx=0.5, rely=0.88, anchor=N)

    col = ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10']
    router_tree_view = Treeview(pop_up, columns=col, show="headings")

    router_tree_view.heading('#1', text='Session ID')
    router_tree_view.heading('#2', text='Start Date')
    router_tree_view.heading('#3', text='Start Time')
    router_tree_view.heading('#4', text='Duration')
    router_tree_view.heading('#5', text='Sets')
    router_tree_view.heading('#6', text='Reps')
    router_tree_view.heading('#7', text='Place')
    router_tree_view.heading('#8', text='Is Planned')
    router_tree_view.heading('#9', text='Exercise Name')
    router_tree_view.heading('#10', text='Day type')

    # Sessions.SessionID, Sessions.StartTime, Sessions.EndTime, SessionDetails.Sets, SessionDetails.Reps, SessionDetails.Sets, SessionDetails.Place, SessionDetails.IsPlanned, Exercises.ExerciseName

    router_tree_view.column("#1", width=70)
    router_tree_view.column("#2", width=70)
    router_tree_view.column("#3", width=70)
    router_tree_view.column("#4", width=70)
    router_tree_view.column("#5", width=70)
    router_tree_view.column("#6", width=40)
    router_tree_view.column("#7", width=40)
    router_tree_view.column("#8", width=50)
    router_tree_view.column("#9", width=70)
    router_tree_view.column("#10", width=90)

    router_tree_view.place(relx=0.5, rely=0.05, anchor=N)

    for i in router_tree_view.get_children():
        router_tree_view.delete(i)

    # (3, 1, 2, 3, 12, 'False', 'home')
    for i in range(len(rows)):
        router_tree_view.insert('', 'end', values=rows[i])


def populate_lists(time_start, date_start, duration, exercise_type, place, day_type, is_planned):
    if is_planned == 1:
        is_planned_word = "True"
    else:
        is_planned_word = "False"

    query = '''SELECT Sessions.SessionID, Sessions.StartDate, Sessions.StartTime, Sessions.Duration, SessionDetails.Sets, 
            SessionDetails.Reps, Sessions.Place, Sessions.IsPlanned, Exercises.ExerciseName, Exercises.Type 
            FROM Sessions INNER JOIN SessionDetails ON Sessions.SessionID = SessionDetails.SessionID 
            INNER JOIN Exercises ON SessionDetails.ExerciseID = Exercises.ExerciseID WHERE IsPlanned = ''' + "'" + is_planned_word + "'"

    # ---------------------------------------------------

    if time_start != "hh:mm:ss" and time_start != "NULL":
        query = query + " AND StartTime = " + "'" + time_start + "'"

    if time_start != "hh:mm:ss" and time_start != "NULL":
        query = query + " AND EndTime = " + "'" + duration + "'"

    # ----------------------------------------------------

    if date_start != "yyyy/mm/dd" and date_start != "NULL":
        query = query + " AND StartDate = " + "'" + date_start + "'"

    # if (du != "yyyy-mm-dd" and du != "NULL"):
    # query = query + " AND EndDate = " + "'" + du + "'"

    # ----------------------------------------------------

    if exercise_type != "Exercise Type" and exercise_type != "NULL":
        query = query + " AND ExerciseName = " + "'" + exercise_type + "'"

    if place != "Place" and place != "NULL":
        query = query + " AND Place = " + "'" + place + "'"

    if day_type != "Day Type" and day_type != "NULL":
        query = query + " AND Type = " + "'" + day_type + "'"

    c.execute(query)
    rows = c.fetchall()
    new_window(rows)


class CalenderSearch(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        var_date_start = StringVar()
        var_duration = StringVar()
        var_time_start = StringVar()
        var_exercise_type = StringVar()
        var_day_type = StringVar()
        var_place = StringVar()

        # bool are 0 and 1
        var_is_Planned = IntVar()

        var_date_start.set("yyyy/mm/dd")

        var_time_start.set("hh:mm:ss")
        var_duration.set("duration")

        var_exercise_type.set("Exercise Type")

        var_day_type.set("Day Type")

        var_place.set("Place")
        var_is_Planned.set(1)

        Types = ["NULL"]
        for row in c.execute('SELECT * FROM Exercises'):
            if row[1] not in Types:
                Types.append(row[1])

        Places = ["NULL"]
        for row in c.execute('SELECT * FROM Sessions'):
            if row[5] not in Places:
                Places.append(row[5])

        Days = ["NULL"]
        for row in c.execute('SELECT * FROM Exercises'):
            if row[2] not in Days:
                Days.append(row[2])

        btn_search = Button(self, text="search",
                            command=lambda: populate_lists(var_time_start.get(), var_date_start.get(),
                                                           var_duration.get(), var_exercise_type.get(), var_place.get(),
                                                           var_day_type.get(), var_is_Planned.get()))
        btn_search.place(relx=0.5, rely=0.7, anchor=N)

        lb_dateStart = Label(self, text="StartDate")
        en_dateStart = Entry(self, textvariable=var_date_start, bd=5)
        lb_dateStart.place(relx=0.35, rely=0.22, anchor=N)
        en_dateStart.place(relx=0.5, rely=0.22, anchor=N)

        # ------------------------------------------------

        lb_timeStart = Label(self, text="StartTime")
        en_timeStart = Entry(self, textvariable=var_time_start, bd=5)
        lb_timeStart.place(relx=0.35, rely=0.06, anchor=N)
        en_timeStart.place(relx=0.5, rely=0.06, anchor=N)

        lb_duration = Label(self, text="Duration")
        en_duration = Entry(self, textvariable=var_duration, bd=5)

        lb_duration.place(relx=0.35, rely=0.14, anchor=N)
        en_duration.place(relx=0.5, rely=0.14, anchor=N)

        # ------------------------------------------------

        op_exType = OptionMenu(self, var_exercise_type, *Types)
        op_exType.config(width=Bwidth - 3, font=('Helvetica', Fsize))
        op_exType.place(relx=0.5, rely=0.38, anchor=N)

        op_place = OptionMenu(self, var_place, *Places)
        op_place.config(width=Bwidth - 3, font=('Helvetica', Fsize))
        op_place.place(relx=0.5, rely=0.46, anchor=N)

        op_daytype = OptionMenu(self, var_day_type, *Days)
        op_daytype.config(width=Bwidth - 3, font=('Helvetica', Fsize))
        op_daytype.place(relx=0.5, rely=0.54, anchor=N)

        cb_IsPlanned = Checkbutton(self, text="Planned", variable=var_is_Planned)
        cb_IsPlanned.place(relx=0.5, rely=0.62, anchor=N)

        btn_close = Button(self, text='X', command=lambda: controller.show_frame(WorkoutCalendar), bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=4)
        btn_close.place(relx=0, rely=0, anchor=NW)


class Settings(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        c.execute("SELECT Reminders FROM User")
        data = c.fetchone()[0]

        var_remind_user = IntVar()
        var_remind_user.set(data)

        page_title = Label(self, text='Settings')
        page_title.place(relx=0.5, rely=0.1, anchor=N)

        def update_notifs():
            c.execute("UPDATE User SET Reminders = ? WHERE UserID = 1", (var_remind_user.get(),))
            conn.commit()

        cb_remind_user = Checkbutton(self, text="Reminders", variable=var_remind_user, command=update_notifs)
        cb_remind_user.place(relx=0.5, rely=0.35, anchor=N)

        btn_add_exercises = Button(self, text="Add Exercises", command=lambda: controller.show_frame(ExerciseListEdit))
        btn_add_exercises.place(relx=0.5, rely=0.25, anchor=N)

        btn_add_exercises = Button(self, text="Edit Profile", command=lambda: controller.show_frame(UserScreenEdit))
        btn_add_exercises.place(relx=0.5, rely=0.45, anchor=N)

        toolbar(self, controller)


class ReminderPopUp(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        page_title = Label(self, text='Workout Reminder', font=("Verdana", 15))
        page_title.place(relx=0.5, rely=0.4, anchor=N)

        page_title = Label(self, text='Your schedule says you should currently be in a workout session', font=("Verdana", 10))
        page_title.place(relx=0.5, rely=0.5, anchor=N)

        btn_close = Button(self, text="I'm busy", command=lambda: controller.show_frame(Profile),
                           bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
        btn_close.place(relx=0.25, rely=0.6, anchor=N)

        btn_close = Button(self, text="I've completed it", command=lambda: controller.show_frame(Profile),
                           bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
        btn_close.place(relx=0.5, rely=0.6, anchor=N)

        btn_close = Button(self, text="I will complete it", command=lambda: controller.show_frame(Profile),
                           bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
        btn_close.place(relx=0.75, rely=0.6, anchor=N)


class WorkoutCalendar(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        CurrentDate = datetime.now()
        self.cal_date = StringVar()

        cal = Calendar(self, selectmode="day", year=CurrentDate.year, month=CurrentDate.month, day=CurrentDate.day,
                       font=("Helvetica", Fsize))
        cal.place(relx=0.5, rely=0.08, anchor=N, width=600, height=420)

        search_btn = Button(self, text='Search', command=lambda: controller.show_frame(CalenderSearch), bg="gray70",
                            bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)

        def both():
            self.cal_date.set(cal.get_date())
            controller.show_frame(SessionScreenInfo)

        load_btn = Button(self, text='Load', command=both, bg="gray70",
                          bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)

        load_btn.place(relx=0.1, rely=0, anchor=NW)
        search_btn.place(relx=0.9, rely=0, anchor=NE)


        toolbar(self, controller)


class SessionScreenInfo(Frame):
    def reset_scroll_region(self, event):
        self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))

    def load_data(self, selected_date):
        st_array = selected_date.split("/")
        if len(st_array[0]) == 1:
            st_array[0] = "0" + st_array[0]

        if len(st_array[1]) == 1:
            st_array[1] = "0" + st_array[1]

        selected_Time = "20" + st_array[2] + "/" + st_array[0] + "/" + st_array[1]

        c.execute(
            "SELECT Sessions.SessionID, Sessions.StartTime, Sessions.Duration, SessionDetails.Sets, SessionDetails.Reps,"
            "Sessions.Place, Sessions.IsPlanned, Exercises.ExerciseName, Exercises.Type, Exercises.CaloriesBurntPerRep * SessionDetails.Reps * SessionDetails.Sets AS TotalCalPerSession, Sessions.StartDate FROM Sessions INNER JOIN SessionDetails ON Sessions.SessionID = "
            "SessionDetails.SessionID INNER JOIN Exercises ON SessionDetails.ExerciseID = Exercises.ExerciseID WHERE StartDate = " + "'" + selected_Time + "'")
        data = c.fetchall()

        c.execute("""SELECT SUM(Exercises.CaloriesBurntPerRep * SessionDetails.Reps * SessionDetails.Sets) AS TotalCalPerExercise FROM Sessions INNER JOIN SessionDetails ON Sessions.SessionID = 
                    SessionDetails.SessionID INNER JOIN Exercises ON SessionDetails.ExerciseID = Exercises.ExerciseID WHERE StartDate = """ + "'" + selected_Time + "'")
        data.insert(0, c.fetchone()[0])

        return data

    def on_show_frame(self, event):
        calendar_page = self.controller.find_page(WorkoutCalendar)
        selected_date = calendar_page.cal_date.get()
        self.data = self.load_data(selected_date)

        self.lb_duration.place_forget()
        self.en_duration_num.place_forget()
        self.lb_calories_burnt.place_forget()
        self.en_calories_burnt.place_forget()
        self.lb_exercise_list.place_forget()
        self.btn_add_data.place_forget()
        self.lb_place.place_forget()
        self.en_place.place_forget()
        self.lb_session_time.place_forget()
        self.my_scrollbar.place_forget()
        self.edit_mode.place_forget()

        if len(self.exercise_list) > 1:
            for i in range(len(self.exercise_list)):
                self.exercise_list[i].grid_forget()
            self.exercise_list = []

        if len(self.data) > 1:
            self.lb_duration.place(relx=0.2, rely=0.35, anchor=N)
            self.en_duration_num.place(relx=0.2, rely=0.42, anchor=N)
            self.lb_calories_burnt.place(relx=0.8, rely=0.35, anchor=N)
            self.en_calories_burnt.place(relx=0.8, rely=0.42, anchor=N)
            self.lb_exercise_list.place(relx=0.08, rely=0.665, anchor=SW)
            self.lb_place.place(relx=0.5, rely=0.35, anchor=N)
            self.en_place.place(relx=0.5, rely=0.42, anchor=N)
            self.lb_session_time.place(relx=0.5, rely=0.20, anchor=N)

            self.var_session_time.set(self.data[1][1] + ":00")
            self.var_sessions_duration.set(self.data[1][2])
            self.var_calories_burnt.set(round(self.data[0]))
            self.var_place.set(self.data[1][5])
            self.edit_mode.place(relx=0.7, rely=0.1, anchor=N)

            self.my_canvas.configure(bg="#B3B3B3", xscrollcommand=self.my_scrollbar.set, bd=-2)
            self.my_scrollbar.bind("<Configure>",
                                   lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))

            max_buttons_onscreen = 5
            if len(self.data) - 1 > max_buttons_onscreen:
                self.my_scrollbar.place(relx=0.5, rely=0.85, width=500, height=20, anchor=N)
            for i in range(len(self.data) - 1):
                self.exercise_list.append(
                    Button(self.second_frame, text=self.data[i + 1][7], command=lambda i=i: send_exercise_id(i + 1),
                           bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), wrap=80, width=8, height=3))
                self.exercise_list[i].grid(row=0, column=i, padx=5)
        else:
            self.btn_add_data.place(relx=0.5, rely=0.5, anchor=N)

        def send_exercise_id(session_details_id):
            self.var_ex_name.set(self.data[session_details_id][7])
            self.var_single_sets.set(self.data[session_details_id][3])
            self.var_single_reps.set(self.data[session_details_id][4])
            self.var_single_type.set(self.data[session_details_id][8])
            self.var_calories_burnt_per.set(round(self.data[session_details_id][9]))
            self.controller.show_frame(SpecificExerciseDetails)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")
        self.bind("<<ShowFrame>>", self.on_show_frame)  # when frame is loaded

        # -----------------------

        self.my_canvas = Canvas(self)
        self.my_canvas.configure(bg="#B3B3B3", bd=-2)
        self.my_canvas.place(relx=0.5, rely=0.7, width=490, height=80, anchor=N)

        self.second_frame = Frame(self.my_canvas)
        self.second_frame.configure(bg="#B3B3B3", bd=5, highlightthickness=0)

        self.my_canvas.create_window((0, 0), window=self.second_frame, anchor=NW)

        self.second_frame.bind("<Configure>", self.reset_scroll_region)

        self.my_scrollbar = Scrollbar(self, orient=HORIZONTAL, command=self.my_canvas.xview)

        # -------------------------

        self.var_session_time = StringVar()
        self.var_sessions_duration = IntVar()

        self.var_calories_burnt = IntVar()
        self.var_calories_burnt_per = IntVar()

        self.var_place = StringVar()

        self.exercise_list = []
        self.data = []

        # send to other frame
        self.var_ex_name = StringVar()
        self.var_single_sets = IntVar()
        self.var_single_reps = IntVar()
        self.var_single_type = StringVar()

        self.lb_session_time = Label(self, textvariable=self.var_session_time, font=("Helvetica", Fsize))

        lb_page_title = Label(self, text="Session Summary", font=("Helvetica", 15))
        lb_page_title.place(relx=0.5, rely=0.1, anchor=N)

        # duration
        self.lb_duration = Label(self, text="Duration", font=("Verdana", 15))
        self.en_duration_num = Entry(self, textvariable=self.var_sessions_duration, justify="center", width=10,
                                     font=("Helvetica", 15), state="disabled")

        self.lb_calories_burnt = Label(self, text="Total Calories Burnt", font=("Verdana", 15))
        self.en_calories_burnt = Entry(self, textvariable=self.var_calories_burnt, justify="center", width=10,
                                       font=("Helvetica", 15), state="disabled")

        self.lb_place = Label(self, text="Place", font=("Verdana", 15))
        self.en_place = Entry(self, textvariable=self.var_place, justify="center", width=10, font=("Helvetica", 15),
                              state="disabled")

        self.lb_exercise_list = Label(self, text="Exercises", font=("Helvetica", 15))

        self.edit_mode = Button(self, text='Edit',
                                command=lambda: self.controller.show_frame(SessionScreenEdit),
                                bg="gray70",
                                bd=3, pady=3, font=("Helvetica", 9), width=5)

        self.btn_add_data = Button(self, text='Add Session Info',
                                   command=lambda: controller.show_frame(AddWorkout), bg="gray70",
                                   bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)

        # ---------------------------------------------------------------------------------------------------

        # close button
        btn_close = Button(self, text='X', command=lambda: controller.show_frame(WorkoutCalendar), bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=4)
        btn_close.place(relx=0, rely=0, anchor=NW)


class SpecificExerciseDetails(Frame):
    def update_data(self):
        InfoPage = self.controller.find_page(SessionScreenInfo)
        self.exercise_name.set("Workout - " + InfoPage.var_ex_name.get())
        self.exercise_sets.set(InfoPage.var_single_sets.get())
        self.exercise_reps.set(InfoPage.var_single_reps.get())
        self.exercise_type.set(InfoPage.var_single_type.get())
        self.var_calories_burnt_per.set(InfoPage.var_calories_burnt_per.get())

    def on_show_frame(self, event):
        self.update_data()

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")
        self.bind("<<ShowFrame>>", self.on_show_frame)  # when frame is loaded

        self.exercise_name = StringVar()
        self.exercise_sets = IntVar()
        self.exercise_reps = IntVar()
        self.exercise_type = StringVar()
        self.var_calories_burnt_per = IntVar()

        lb_exercise_name = Label(self, textvariable=self.exercise_name)
        lb_exercise_name.place(relx=0.1, rely=0.15, anchor=W)

        lb_exercise_name = Label(self, text="Reps")
        lb_exercise_name.place(relx=0.1, rely=0.30, anchor=W)

        en_exercise_name = Entry(self, textvariable=self.exercise_reps, state="disabled")
        en_exercise_name.place(relx=0.4, rely=0.30, anchor=W)

        lb_exercise_sets = Label(self, text="Sets")
        lb_exercise_sets.place(relx=0.1, rely=0.35, anchor=W)

        en_exercise_sets = Entry(self, textvariable=self.exercise_sets, state="disabled")
        en_exercise_sets.place(relx=0.4, rely=0.35, anchor=W)

        lb_exercise_sets = Label(self, text="Calories Burnt")
        lb_exercise_sets.place(relx=0.1, rely=0.45, anchor=W)

        en_exercise_sets = Entry(self, textvariable=self.var_calories_burnt_per, state="disabled")
        en_exercise_sets.place(relx=0.4, rely=0.45, anchor=W)

        lb_exercise_sets = Label(self, text="Exercise Type")
        lb_exercise_sets.place(relx=0.1, rely=0.60, anchor=W)

        en_exercise_sets = Entry(self, textvariable=self.exercise_type, state="disabled")
        en_exercise_sets.place(relx=0.4, rely=0.60, anchor=W)

        btn_close = Button(self, text='X', command=lambda: controller.show_frame(SessionScreenInfo), bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
        btn_close.grid(row=3, column=2)


class SessionScreenEdit(Frame):
    def fetch_details(self):
        calendar_page = self.controller.find_page(SessionScreenInfo)
        self.data = calendar_page.data

        for i in self.router_tree_view.get_children():
            self.router_tree_view.delete(i)

        for i in range(len(self.data) - 1):
            row = [self.data[i + 1][7], self.data[i + 1][3], self.data[i + 1][4]]
            self.router_tree_view.insert('', 'end', values=row)

        self.var_date_start.set(self.data[1][10])
        self.var_time_start.set(self.data[1][1])
        self.var_session_duration.set(self.data[1][2])
        self.var_session_place.set(self.data[1][5])
        IsPlanned = 0
        if self.data[1][6] == "True":
            IsPlanned = 1
        self.var_is_Planned.set(IsPlanned)

        def select_exercise(event):
            index = self.router_tree_view.selection()[0]
            selected_item = self.router_tree_view.item(index)['values']
            self.var_exercise_name.set(selected_item[0])
            self.var_exercise_sets.set(selected_item[1])
            self.var_exercise_reps.set(selected_item[2])

        self.router_tree_view.bind('<<TreeviewSelect>>', select_exercise)

    def on_show_frame(self, event):
        self.fetch_details()

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")
        self.bind("<<ShowFrame>>", self.on_show_frame)  # when frame is loaded

        def add_exercise():
            double = False
            for i in self.router_tree_view.get_children():
                values = self.router_tree_view.item(i, 'values')
                if values[0] == self.var_exercise_name.get():
                    double = True
            if self.var_exercise_sets.get() < 1 or self.var_exercise_reps.get() < 1 or self.var_exercise_name.get() == "Exercise Name" or double == True:
                messagebox.showerror('Invalid Fields',
                                     'Must be a valid exercise and number of sets and reps, no repeating exercises')
            else:
                insert_row = [self.var_exercise_name.get(), self.var_exercise_sets.get(), self.var_exercise_reps.get()]
                self.router_tree_view.insert('', 'end', values=insert_row)

        def delete_exercise():
            try:
                selected_item = self.router_tree_view.selection()
                self.router_tree_view.delete(selected_item[0])
            except IndexError:
                pass

        def save_changes():
            # update session
            IsPlanned = "False"
            if self.var_is_Planned.get() == 1:
                IsPlanned = "True"
            c.execute(
                "UPDATE Sessions SET StartDate = ?, StartTime = ?, Duration = ?, Place = ?, IsPlanned = ? WHERE SessionID = ?",
                (self.var_date_start.get(), self.var_time_start.get(), self.var_session_duration.get(),
                 self.var_session_place.get(), IsPlanned, self.data[1][0]))

            # delete current exercises
            c.execute("DELETE FROM SessionDetails WHERE SessionID=?", (self.data[1][0],))

            # then add all
            for i in self.router_tree_view.get_children():
                c.execute('SELECT ExerciseID FROM Exercises WHERE ExerciseName = ?',
                          (self.router_tree_view.item(i)['values'][0],))
                ex_id = c.fetchone()[0]

                c.execute("SELECT SessionDetailsID FROM SessionDetails ORDER BY SessionDetailsID DESC LIMIT 1")
                last_SessionDetailsID = c.fetchone()[0]
                c.execute("INSERT INTO SessionDetails VALUES (?, ?, ?, ?, ?)",
                          (
                              last_SessionDetailsID + 1, self.data[1][0], ex_id,
                              self.router_tree_view.item(i)['values'][1],
                              self.router_tree_view.item(i)['values'][2]))
            conn.commit()
            self.controller.show_frame(WorkoutCalendar)

        self.var_date_start = StringVar()
        self.var_time_start = StringVar()
        self.var_session_duration = IntVar()
        self.var_session_place = StringVar()
        self.var_is_Planned = IntVar()

        self.var_exercise_name = StringVar()
        self.var_exercise_name.set("Exercise Name")
        self.var_exercise_sets = IntVar()
        self.var_exercise_reps = IntVar()
        self.data = []

        lb_timeStart = Label(self, text="Start Date")
        en_timeStart = Entry(self, textvariable=self.var_date_start, bd=5)
        lb_timeStart.place(relx=0.18, rely=0.13, anchor=NE)
        en_timeStart.place(relx=0.3, rely=0.13, anchor=N)

        lb_timeStart = Label(self, text="Start Time")
        en_timeStart = Entry(self, textvariable=self.var_time_start, bd=5)
        lb_timeStart.place(relx=0.68, rely=0.13, anchor=NE)
        en_timeStart.place(relx=0.8, rely=0.13, anchor=N)

        lb_timeStart = Label(self, text="Duration")
        en_timeStart = Entry(self, textvariable=self.var_session_duration, bd=5)
        lb_timeStart.place(relx=0.18, rely=0.23, anchor=NE)
        en_timeStart.place(relx=0.3, rely=0.23, anchor=N)

        lb_timeStart = Label(self, text="Place")
        en_timeStart = Entry(self, textvariable=self.var_session_place, bd=5)
        lb_timeStart.place(relx=0.68, rely=0.23, anchor=NE)
        en_timeStart.place(relx=0.8, rely=0.23, anchor=N)

        cb_IsPlanned = Checkbutton(self, text="Planned", variable=self.var_is_Planned)
        cb_IsPlanned.place(relx=0.5, rely=0.3, anchor=N)

        exercise_list = []
        for row in c.execute('SELECT * FROM Exercises'):
            if row[1] not in exercise_list:
                exercise_list.append(row[1])

        op_exType = OptionMenu(self, self.var_exercise_name, *exercise_list)
        op_exType.config(width=14, font=('Helvetica', Fsize))
        op_exType.place(relx=0.23, rely=0.4, anchor=W)

        lb_timeStart = Label(self, text="Sets")
        en_timeStart = Entry(self, textvariable=self.var_exercise_sets, bd=5, width=5)
        lb_timeStart.place(relx=0.53, rely=0.4, anchor=W)
        en_timeStart.place(relx=0.58, rely=0.4, anchor=W)

        lb_timeStart = Label(self, text="Reps")
        en_timeStart = Entry(self, textvariable=self.var_exercise_reps, bd=5, width=5)
        lb_timeStart.place(relx=0.73, rely=0.4, anchor=W)
        en_timeStart.place(relx=0.78, rely=0.4, anchor=W)

        btn_year_show = Button(self, text='Remove Exercise', bg="gray70", command=delete_exercise,
                               bd=3, pady=2, width=20)
        btn_year_show.place(relx=0.65, rely=0.45, anchor=N)

        btn_year_show = Button(self, text='Add Exercise', bg="gray70", command=add_exercise,
                               bd=3, pady=2, width=20)
        btn_year_show.place(relx=0.35, rely=0.45, anchor=N)

        col = ['test1', 'test2', 'test3']
        self.router_tree_view = Treeview(self, columns=col, show="headings")

        self.router_tree_view.heading('#1', text='Exercise Name')
        self.router_tree_view.heading('#2', text='Sets')
        self.router_tree_view.heading('#3', text='Reps')

        self.router_tree_view.column("#1", width=50)
        self.router_tree_view.column("#2", width=15)
        self.router_tree_view.column("#3", width=15)

        self.router_tree_view.place(relx=0.5, rely=0.52, anchor=N, width=500, height=150)

        btn_create_routine = Button(self, text="Save", bg="gray70", command=save_changes,
                                    bd=3, pady=2, font=("Helvetica", Fsize), width=12)
        btn_create_routine.place(relx=0.7, rely=0.82, anchor=N)

        btn_create_routine = Button(self, text="Cancel", bg="gray70",
                                    command=lambda: controller.show_frame(SessionScreenInfo),
                                    bd=3, pady=2, font=("Helvetica", Fsize), width=12)
        btn_create_routine.place(relx=0.3, rely=0.82, anchor=N)


class AddExercise(Frame):
    def fetch_exercises(self):
        for i in self.router_tree_view.get_children():
            self.router_tree_view.delete(i)

        c.execute("SELECT * FROM Exercises")
        data = c.fetchall()
        print(data)
        for i in range(len(data)):
            self.router_tree_view.insert('', 'end', values=data[i])

    def on_show_frame(self, event):
        self.fetch_exercises()

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")
        self.bind("<<ShowFrame>>", self.on_show_frame)  # when frame is loaded

        var_exercise_name = StringVar()
        var_day_type = StringVar()
        var_calories_per = IntVar()

        def update_exercises():

            c.execute("DELETE FROM Exercises")

            for i in self.router_tree_view.get_children():
                c.execute("SELECT ExerciseID FROM Exercises ORDER BY ExerciseID DESC LIMIT 1")
                last_ExercisesID = c.fetchone()[0]
                c.execute("INSERT INTO Exercises VALUES (?, ?, ?, ?)",
                          (last_ExercisesID + 1, self.router_tree_view.item(i)['values'][1],
                           self.router_tree_view.item(i)['values'][2], self.router_tree_view.item(i)['values'][3]))
            conn.commit()
            self.controller.show_frame(WorkoutCalendar)

        def add_exercise():
            c.execute("SELECT ExerciseID FROM Exercises ORDER BY ExerciseID DESC LIMIT 1")
            last_ExercisesID = c.fetchone()[0]
            calories_per = ((var_calories_per.get() / 60) * 0.75)
            row = [last_ExercisesID + 1, var_exercise_name.get(), var_day_type.get(), calories_per]
            self.router_tree_view.insert('', 'end', values=row)

        def delete_exercise():
            try:
                selected_item = self.router_tree_view.selection()
                self.router_tree_view.delete(selected_item[0])
            except IndexError:
                pass

        lb_timeStart = Label(self, text="Exercise Name")
        en_timeStart = Entry(self, textvariable=var_exercise_name, bd=5, width=15)
        lb_timeStart.place(relx=0.3, rely=0.03, anchor=N)
        en_timeStart.place(relx=0.3, rely=0.08, anchor=N)

        lb_timeStart = Label(self, text="Day Type")
        en_timeStart = Entry(self, textvariable=var_day_type, bd=5, width=15)
        lb_timeStart.place(relx=0.5, rely=0.03, anchor=N)
        en_timeStart.place(relx=0.5, rely=0.08, anchor=N)

        lb_timeStart = Label(self, text="Calories burnt in 10 mins")
        en_timeStart = Entry(self, textvariable=var_calories_per, bd=5, width=15)
        lb_timeStart.place(relx=0.70, rely=0.03, anchor=N)
        en_timeStart.place(relx=0.70, rely=0.08, anchor=N)

        btn_year_show = Button(self, text='Remove Exercise', bg="gray70", command=delete_exercise,
                               bd=3, pady=2, width=21)
        btn_year_show.place(relx=0.35, rely=0.15, anchor=N)

        btn_year_show = Button(self, text='Add Exercise', bg="gray70", command=add_exercise,
                               bd=3, pady=2, width=21)
        btn_year_show.place(relx=0.65, rely=0.15, anchor=N)

        col = ['test1', 'test2', 'test3', 'test4']
        self.router_tree_view = Treeview(self, columns=col, show="headings")

        self.router_tree_view.heading('#1', text='ID')
        self.router_tree_view.heading('#2', text='Exercise Name')
        self.router_tree_view.heading('#3', text='Day Type')
        self.router_tree_view.heading('#4', text='Calories per rep')

        self.router_tree_view.column("#1", width=10)
        self.router_tree_view.column("#2", width=60)
        self.router_tree_view.column("#3", width=60)
        self.router_tree_view.column("#4", width=5)

        self.router_tree_view.place(relx=0.5, rely=0.22, anchor=N, width=500, height=340)

        btn_create_routine = Button(self, text="Save changes", bg="gray70", command=update_exercises,
                                    bd=3, font=("Helvetica", Fsize), width=18)
        btn_create_routine.place(relx=0.65, rely=0.85, anchor=N)

        btn_create_routine = Button(self, text="Cancel", bg="gray70", command=lambda: controller.show_frame(Settings),
                                    bd=3, font=("Helvetica", Fsize), width=18)
        btn_create_routine.place(relx=0.35, rely=0.85, anchor=N)

        toolbar(self, controller)


class UserScreenEdit(Frame):
    def on_show_frame(self, event):
        user_page = self.controller.find_page(Profile)
        user_data = user_page.User_Data
        self.var_last_name.set(user_data[0][1])
        self.var_first_name.set(user_data[0][2])
        self.var_dob.set(user_data[0][3])
        self.var_weight.set(user_data[0][4])
        self.var_target_weight.set(user_data[0][5])
        self.var_height.set(user_data[0][6])
        self.var_gender.set(user_data[0][7])
        print(user_data)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")
        self.bind("<<ShowFrame>>", self.on_show_frame)  # when frame is loaded

        self.var_last_name = StringVar()
        self.var_first_name = StringVar()
        self.var_dob = StringVar()
        self.var_weight = IntVar()
        self.var_target_weight = IntVar()
        self.var_height = IntVar()
        self.var_gender = StringVar()

        lb_first_name = Label(self, text="First name")
        en_first_name = Entry(self, textvariable=self.var_first_name)
        lb_first_name.place(relx=0.43, rely=0.15, anchor=E)
        en_first_name.place(relx=0.65, rely=0.15, anchor=E)

        lb_last_name = Label(self, text="Last name")
        en_last_name = Entry(self, textvariable=self.var_last_name)
        lb_last_name.place(relx=0.43, rely=0.25, anchor=E)
        en_last_name.place(relx=0.65, rely=0.25, anchor=E)

        lb_DoB = Label(self, text="Date of Birth")
        en_DoB = Entry(self, textvariable=self.var_dob)
        lb_DoB.place(relx=0.43, rely=0.35, anchor=E)
        en_DoB.place(relx=0.65, rely=0.35, anchor=E)

        lb_weight = Label(self, text="Weight")
        en_weight = Entry(self, textvariable=self.var_weight)
        lb_weight.place(relx=0.43, rely=0.45, anchor=E)
        en_weight.place(relx=0.65, rely=0.45, anchor=E)

        lb_target_weight = Label(self, text="Target Weight")
        en_target_weight = Entry(self, textvariable=self.var_target_weight)
        lb_target_weight.place(relx=0.43, rely=0.55, anchor=E)
        en_target_weight.place(relx=0.65, rely=0.55, anchor=E)

        lb_height = Label(self, text="Height")
        en_height = Entry(self, textvariable=self.var_height)
        lb_height.place(relx=0.43, rely=0.65, anchor=E)
        en_height.place(relx=0.65, rely=0.65, anchor=E)

        lb_gender = Label(self, text="Gender")
        en_gender = Entry(self, textvariable=self.var_gender)
        lb_gender.place(relx=0.43, rely=0.75, anchor=E)
        en_gender.place(relx=0.65, rely=0.75, anchor=E)

        def save_changes():
            c.execute(
                "UPDATE User SET LastName = ?, FirstName = ?, DoB = ?, Weight = ?, TargetWeight = ?, Height = ?, Gender = ? WHERE UserID = 1",
                (self.var_last_name.get(), self.var_first_name.get(), self.var_dob.get(), self.var_weight.get(),
                 self.var_target_weight.get(), self.var_height.get(), self.var_gender.get()))
            conn.commit()
            controller.show_frame(Profile)

        btn_create_routine = Button(self, text="Save", bg="gray70", command=save_changes,
                                    bd=3, pady=2, font=("Helvetica", Fsize), width=12)
        btn_create_routine.place(relx=0.7, rely=0.82, anchor=N)

        btn_create_routine = Button(self, text="Cancel", bg="gray70",
                                    command=lambda: controller.show_frame(Settings),
                                    bd=3, pady=2, font=("Helvetica", Fsize), width=12)
        btn_create_routine.place(relx=0.3, rely=0.82, anchor=N)


class ExerciseListEdit(Frame):
    def on_show_frame(self, event):
        print()

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")
        self.bind("<<ShowFrame>>", self.on_show_frame)  # when frame is loaded

        var_exercise_name = StringVar()
        var_exercise_type = StringVar()
        var_exercise_cals = StringVar()

        lb_exercise_name = Label(self, text="Exercise Name")
        en_exercise_name = Entry(self, textvariable=var_exercise_name)
        lb_exercise_name.place(relx=0.13, rely=0.15, anchor=E)
        en_exercise_name.place(relx=0.35, rely=0.15, anchor=E)

        lb_exercise_type = Label(self, text="Exercise type")
        en_exercise_type = Entry(self, textvariable=var_exercise_type)
        lb_exercise_type.place(relx=0.43, rely=0.15, anchor=E)
        en_exercise_type.place(relx=0.65, rely=0.15, anchor=E)

        lb_exercise_cals = Label(self, text="Calories burnt per 12")
        en_exercise_cals = Entry(self, textvariable=var_exercise_cals)
        lb_exercise_cals.place(relx=0.73, rely=0.15, anchor=E)
        en_exercise_cals.place(relx=0.95, rely=0.15, anchor=E)

        def add_exercise():
            c.execute("SELECT ExerciseID FROM Exercises ORDER BY ExerciseID DESC LIMIT 1")
            last_ExercisesID = c.fetchone()[0]

            calories_per = (var_exercise_cals.get() / 12)
            row = [last_ExercisesID + 1, var_exercise_name.get(), var_exercise_type.get(), calories_per]
            self.router_tree_view.insert('', 'end', values=row)

        def save_changes():
            c.execute(
                "INSERT INTO SessionDetails VALUES (?, ?, ?, ?)",
                (1, var_exercise_name.get(), var_exercise_type.get(), var_exercise_cals.get()))# get next id
            conn.commit()
            controller.show_frame(Profile)

        col = ['test1', 'test2', 'test3', 'test4']
        self.router_tree_view = Treeview(self, columns=col, show="headings")

        self.router_tree_view.heading('#1', text='ID')
        self.router_tree_view.heading('#2', text='Exercise Name')
        self.router_tree_view.heading('#3', text='Day Type')
        self.router_tree_view.heading('#4', text='Calories per rep')

        self.router_tree_view.column("#1", width=10)
        self.router_tree_view.column("#2", width=60)
        self.router_tree_view.column("#3", width=60)
        self.router_tree_view.column("#4", width=5)

        self.router_tree_view.place(relx=0.5, rely=0.22, anchor=N, width=500, height=340)

        btn_create_routine = Button(self, text="Save", bg="gray70", command=save_changes,
                                    bd=3, pady=2, font=("Helvetica", Fsize), width=12)
        btn_create_routine.place(relx=0.7, rely=0.82, anchor=N)

        btn_create_routine = Button(self, text="Cancel", bg="gray70",
                                    command=lambda: controller.show_frame(Settings),
                                    bd=3, pady=2, font=("Helvetica", Fsize), width=12)
        btn_create_routine.place(relx=0.3, rely=0.82, anchor=N)


app = tkinterApp()
app.mainloop()
