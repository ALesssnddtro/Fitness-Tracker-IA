from tkinter import *
from tkcalendar import *
from tkinter.ttk import Treeview
import tkcalendar
import sqlite3
from datetime import datetime
from datetime import timedelta

LARGEFONT = ("Verdana", 35)
Bwidth = 12
Fsize = 11

def ReminderCheck():

    Notif = False

    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    CurrentDate = datetime.now()

    for row in c.execute('SELECT * FROM Sessions'):
        Duration = row[4]
        CurrentDate = CurrentDate.strftime("%Y/%m/%d %I:%M %p")
        CurrentDate = datetime.strptime(CurrentDate, "%Y/%m/%d %H:%M %p")

        ExpectedDateMin = row[2] + " " + row[3]
        ExpectedDateMin = datetime.strptime(ExpectedDateMin, "%Y/%m/%d %I:%M")
        ExpectedDateMax = ExpectedDateMin + timedelta(minutes=Duration)

        #print(CurrentDate, ExpectedDateMin, ExpectedDateMax)

        if CurrentDate > ExpectedDateMin and CurrentDate < ExpectedDateMax:
            Notif = True

    return Notif

class tkinterApp(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.shared_data = {
            "Remind": IntVar(),
            "FirstStartUp": IntVar()
        }

        self.shared_data["Remind"].set(1)

        #print(self.shared_data["Remind"].get())

        self.geometry("600x500")
        self.resizable(width=False, height=False)
        self.title("Fitness Tracker")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (NewUser, Profile, DailyActivity, AddWorkout, CalenderSearch, Settings, ReminderPopUp, WorkoutCalendar, SessionInfoScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        RemindInt = self.shared_data["Remind"].get()
        if ReminderCheck() and (RemindInt == 1):
            self.show_frame(ReminderPopUp)
        else:
            self.show_frame(Profile)

        #print(self.shared_data["Remind"].get())

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def find_page(self, page_class):
        return self.frames[page_class]


def toolbar(self, controller):
    button_plus = Button(self, text='Calender', command=lambda: controller.show_frame(WorkoutCalendar), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    # button_plus.grid(row=10, column=0, sticky=W)
    button_plus.place(relx=0.1, rely=1, anchor=S)

    button_plus = Button(self, text='DailyActivity', command=lambda: controller.show_frame(DailyActivity), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    # button_plus.grid(row=10, column=1, sticky=W)
    button_plus.place(relx=0.3, rely=1, anchor=S)

    button_plus = Button(self, text='+', command=lambda: controller.show_frame(AddWorkout), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    # button_plus.grid(row=10, column=2, sticky=W)
    button_plus.place(relx=0.5, rely=1, anchor=S)

    button_plus = Button(self, text='Profile', command=lambda: controller.show_frame(Profile), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    # button_plus.grid(row=10, column=3, sticky=W)
    button_plus.place(relx=0.7, rely=1, anchor=S)

    button_plus = Button(self, text='Settings', command=lambda: controller.show_frame(Settings), bg="gray70",
                         bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
    # button_plus.grid(row=10, column=4, sticky=W)
    button_plus.place(relx=0.9, rely=1, anchor=S)


class NewUser(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        name_text = StringVar()
        name_label = Label(self, text='USER NULL')
        name_label.grid(row=3, column=0, sticky=E)

        toolbar(self, controller)


class Profile(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        name_text = StringVar()
        name_label = Label(self, text='USER NULL')
        name_label.grid(row=3, column=0, sticky=E)

        toolbar(self, controller)


# second window frame page1
class DailyActivity(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        toolbar(self, controller)


# third window frame page2
class AddWorkout(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        var_sessions_length = IntVar()
        var_sessions_index = IntVar()
        var_sessions_index.set(0)
        var_sessions_id = IntVar()
        var_sessions_trained = StringVar()
        var_sessions_burnt = IntVar()
        var_sessions_reps = IntVar()
        var_sessions_start = StringVar()
        var_sessions_end = StringVar()

        def nav_left():
            print("l")

        def nav_right():
            print("r")

        left_btn = Button(self, text='<', width=3, command=nav_left)
        left_btn.grid(row=3, column=1)

        # Right Arrow
        right_btn = Button(self, text='>', width=3, command=nav_right)
        right_btn.grid(row=3, column=2)

        # ID
        id_text = StringVar()
        id_label = Label(self, text='ID', width=Bwidth)
        id_label.grid(row=1, column=0)
        id_entry = Entry(self, textvariable=var_sessions_id, width=Bwidth)
        id_entry.grid(row=1, column=1)

        # MusclesTrained
        trained_text = StringVar()
        trained_label = Label(self, text='Muscles Trained', width=Bwidth)
        trained_label.grid(row=1, column=2)
        trained_entry = Entry(self, textvariable=var_sessions_trained, width=Bwidth)
        trained_entry.grid(row=1, column=3)

        # CaloriesBurnt
        burnt_text = StringVar()
        burnt_label = Label(self, text='Calories Burnt', width=Bwidth)
        burnt_label.grid(row=2, column=0)
        burnt_entry = Entry(self, textvariable=var_sessions_burnt, width=Bwidth)
        burnt_entry.grid(row=2, column=1)

        # Reps
        reps_text = StringVar()
        reps_label = Label(self, text='Reps', width=Bwidth)
        reps_label.grid(row=2, column=2)
        reps_entry = Entry(self, textvariable=var_sessions_reps, width=Bwidth)
        reps_entry.grid(row=2, column=3)

        # StartTime
        start_text = StringVar()
        start_label = Label(self, text='StartTime', width=Bwidth)
        start_label.grid(row=3, column=0)
        start_entry = Entry(self, textvariable=var_sessions_start, width=Bwidth)
        start_entry.grid(row=3, column=1)

        # EndTime
        end_text = StringVar()
        end_label = Label(self, text='EndTime', width=Bwidth)
        end_label.grid(row=3, column=2)
        end_entry = Entry(self, textvariable=var_sessions_end, width=Bwidth)
        end_entry.grid(row=3, column=3)

        add_btn = Button(self, text='Add Session', width=Bwidth)
        add_btn.grid(row=5, column=0)

        remove_btn = Button(self, text='Remove Session', width=Bwidth)
        remove_btn.grid(row=5, column=1)

        update_btn = Button(self, text='Update Session', width=Bwidth)
        update_btn.grid(row=5, column=2)

        clear_btn = Button(self, text='Clear Input', width=Bwidth)
        clear_btn.grid(row=5, column=3)
        toolbar(self, controller)


def new_window(rows):
    pop_up = Toplevel()
    pop_up.geometry("750x280")
    pop_up.title("data")
    btn_button = Button(pop_up, text="close", command=lambda: pop_up.destroy())
    btn_button.place(relx=0.5, rely=0.88, anchor=N)

    col = ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10']
    router_tree_view = Treeview(pop_up, columns=col, show="headings")

    router_tree_view.heading('#1', text='SessionID')
    router_tree_view.heading('#2', text='StartDate')
    router_tree_view.heading('#3', text='StartTime')
    router_tree_view.heading('#4', text='Duration')
    router_tree_view.heading('#5', text='Sets')
    router_tree_view.heading('#6', text='Reps')
    router_tree_view.heading('#7', text='Place')
    router_tree_view.heading('#8', text='IsPlanned')
    router_tree_view.heading('#9', text='ExerciseName')
    router_tree_view.heading('#10', text='Daytype')

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

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    for i in router_tree_view.get_children():
        router_tree_view.delete(i)

    # (3, 1, 2, 3, 12, 'False', 'home')
    for i in range(len(rows)):
        router_tree_view.insert('', 'end', values=rows[i])


def populatelists(ts, ds, du, et, p, dt, pl):
    true_pl = "True"
    if pl == 1:
        true_pl = "True"
    else:
        true_pl = "False"

    query = "SELECT Sessions.SessionID, Sessions.StartDate, Sessions.StartTime, Sessions.Duration, SessionDetails.Sets, " \
            "SessionDetails.Reps, SessionDetails.Place, SessionDetails.IsPlanned, Exercises.ExerciseName, Exercises.Type " \
            "FROM Sessions INNER JOIN SessionDetails ON Sessions.SessionID = SessionDetails.SessionID " \
            "INNER JOIN Exercises ON SessionDetails.ExerciseID = Exercises.ExerciseID WHERE IsPlanned = " + "'" + true_pl + "'"
    # print(query)

    # ---------------------------------------------------

    if (ts != "hh:mm:ss" and ts != "NULL"):
        query = query + " AND StartTime = " + "'" + ts + "'"

    if (ts != "hh:mm:ss" and ts != "NULL"):
        query = query + " AND EndTime = " + "'" + du + "'"

    # ----------------------------------------------------

    if (ds != "yyyy-mm-dd" and ds != "NULL"):
        query = query + " AND StartDate = " + "'" + ds + "'"

    if (du != "yyyy-mm-dd" and du != "NULL"):
        query = query + " AND EndDate = " + "'" + du + "'"

    # ----------------------------------------------------

    if (et != "Exercise Type" and et != "NULL"):
        query = query + " AND ExerciseName = " + "'" + et + "'"

    if (p != "Place" and p != "NULL"):
        query = query + " AND Place = " + "'" + p + "'"

    if (dt != "Day Type" and dt != "NULL"):
        query = query + " AND Type = " + "'" + dt + "'"

    #print(query)

    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    new_window(rows)
    # print(rows)


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

        var_reps = IntVar()
        var_sets = IntVar()

        var_date_start.set("yyyy-mm-dd")

        var_time_start.set("hh:mm:ss")
        var_duration.set("duration")

        var_exercise_type.set("Exercise Type")

        var_day_type.set("Day Type")

        var_place.set("Place")
        var_is_Planned.set(1)

        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        Types = ["NULL"]
        for row in c.execute('SELECT * FROM Exercises'):
            if row[1] not in Types:
                Types.append(row[1])

        Places = ["NULL"]
        for row in c.execute('SELECT * FROM SessionDetails'):
            if row[6] not in Places:
                Places.append(row[6])

        Days = ["NULL"]
        for row in c.execute('SELECT * FROM Exercises'):
            if row[2] not in Days:
                Days.append(row[2])

        btn_search = Button(self, text="search",
                            command=lambda: populatelists(var_time_start.get(), var_date_start.get(),
                                                          var_duration.get(), var_exercise_type.get(), var_place.get(),
                                                          var_day_type.get(), var_is_Planned.get()))
        btn_search.place(relx=0.5, rely=0.7, anchor=N)

        lb_dateStart = Label(self, text="StartDate")
        en_dateStart = Entry(self, textvariable=var_date_start, bd=5)
        # dateStart.grid(row=2, column=0)
        # EdateStart.grid(row=2, column=1)
        lb_dateStart.place(relx=0.35, rely=0.22, anchor=N)
        en_dateStart.place(relx=0.5, rely=0.22, anchor=N)

        # ------------------------------------------------

        lb_timeStart = Label(self, text="StartTime")
        en_timeStart = Entry(self, textvariable=var_time_start, bd=5)
        # dateStart.grid(row=2, column=0)
        # EdateStart.grid(row=2, column=1)
        lb_timeStart.place(relx=0.35, rely=0.06, anchor=N)
        en_timeStart.place(relx=0.5, rely=0.06, anchor=N)

        lb_timeEnd = Label(self, text="EndTime")
        en_timeEnd = Entry(self, textvariable=var_duration, bd=5)
        # dateEnd.grid(row=2, column=3)
        # EdateEnd.grid(row=2, column=4)
        lb_timeEnd.place(relx=0.35, rely=0.14, anchor=N)
        en_timeEnd.place(relx=0.5, rely=0.14, anchor=N)

        # ------------------------------------------------

        op_exType = OptionMenu(self, var_exercise_type, *Types)
        op_exType.config(width=Bwidth - 3, font=('Helvetica', Fsize))
        # type.grid(row=3, column=2)
        op_exType.place(relx=0.5, rely=0.38, anchor=N)

        op_place = OptionMenu(self, var_place, *Places)
        op_place.config(width=Bwidth - 3, font=('Helvetica', Fsize))
        # place.grid(row=4, column=2)
        op_place.place(relx=0.5, rely=0.46, anchor=N)

        op_daytype = OptionMenu(self, var_day_type, *Days)
        op_daytype.config(width=Bwidth - 3, font=('Helvetica', Fsize))
        # Intensity.grid(row=5, column=2)
        op_daytype.place(relx=0.5, rely=0.54, anchor=N)

        cb_IsPlanned = Checkbutton(self, text="Planned", variable=var_is_Planned)
        # Reminders.grid(row=6, column=2)
        cb_IsPlanned.place(relx=0.5, rely=0.62, anchor=N)

        # SpinTestDay = Spinbox(self, from_ = 1, to = 31, width=4)
        # SpinTestDay.place(relx=0.4, rely=0.70, anchor=N)

        # SpinTestMonth = Spinbox(self, from_ = 1, to = 12, width=4)
        # SpinTestMonth.place(relx=0.5, rely=0.70, anchor=N)

        # SpinTestYear = Spinbox(self, from_ = 2000, to = 2020, width=4)
        # SpinTestYear.place(relx=0.6, rely=0.70, anchor=N)

        exit_btn = Button(self, text='Ignore', command=lambda: controller.show_frame(WorkoutCalendar), bg="gray70",
                          bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
        exit_btn.pack()

class Settings(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")



        vars_remind_user = IntVar(self)
        vars_remind_user.set(self.controller.shared_data["Remind"].get())

        RemindersLabel = Label(self, text='Settings')
        RemindersLabel.grid(row=1, column=2)
        Reminders = Checkbutton(self, text="RemindUser", variable=vars_remind_user)
        Reminders.grid(row=4, column=2)
        left_btn = Button(self, text='x', width=3)
        left_btn.grid(row=3, column=2)

        self.controller.shared_data["Remind"].set(vars_remind_user.get())

        toolbar(self, controller)


class ReminderPopUp(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        x = self.controller.shared_data["Remind"].get()

        btn_close = Button(self, text='Ignore', command=lambda: controller.show_frame(Profile), bg="gray70",
               bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)
        btn_close.grid(row=3, column=2)
        #command = lambda: controller.show_frame(Profile)


class WorkoutCalendar(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        CurrentDate = datetime.now()
        self.caldate = StringVar()


        cal = Calendar(self, selectmode="day", year=CurrentDate.year, month=CurrentDate.month, day=CurrentDate.day,
                       font=("Helvetica", Fsize))

        print(cal.get_date())



        search_btn = Button(self, text='Search', command=lambda: controller.show_frame(CalenderSearch), bg="gray70",
               bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)



        def both():
            self.caldate.set(cal.get_date())
            loaddate(self.caldate.get())

        load_btn = Button(self, text='Load', command=both, bg="gray70",
                          bd=3, pady=5, font=("Helvetica", Fsize), width=Bwidth)


        load_btn.place(relx=0.1, rely=0, anchor=NW)
        search_btn.place(relx=0.9, rely=0, anchor=NE)

        cal.place(relx=0.5, rely=0.08, anchor=N, width=600, height=420)




        toolbar(self, controller)


def loaddate(selected_Time):

    print(selected_Time, "a")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    st_array = selected_Time.split("/")
    if len(st_array[0]) == 1:
        st_array[0] = "0" + st_array[0]

    if len(st_array[1]) == 1:
        st_array[1] = "0" + st_array[1]

    selected_Time = "20" + st_array[2] + "/" + st_array[0] + "/" + st_array[1]

    print(selected_Time, "b")

    c.execute("SELECT Sessions.SessionID, Sessions.StartDate, Sessions.StartTime, Sessions.Duration, SessionDetails.Sets, "
              "SessionDetails.Reps, SessionDetails.Place, SessionDetails.IsPlanned, Exercises.ExerciseName, Exercises.Type "
              "FROM Sessions INNER JOIN SessionDetails ON Sessions.SessionID = SessionDetails.SessionID "
              "INNER JOIN Exercises ON SessionDetails.ExerciseID = Exercises.ExerciseID WHERE StartDate = " + "'" + selected_Time + "'")
    data = c.fetchall()
    new_window(data)


class SessionInfoScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3B3B3")

        calendarpage = self.controller.find_page(WorkoutCalendar)

        selecteddate = calendarpage.caldate.get()
        print("#------------------------#")



        btn_close = Button(self, text='X', command=lambda: controller.show_frame(WorkoutCalendar), bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=4)
        btn_close.place(relx=0, rely=0, anchor=NW)



        btn_left = Button(self, text='<', bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=4)
        btn_left.place(relx=0.15, rely=0, anchor=NW)

        btn_right = Button(self, text='>', bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=4)
        btn_right.place(relx=0.85, rely=0, anchor=NE)

        lb_duration = Label(self, text="")
        lb_duration.place(relx=0.1, rely=0.2, anchor=S)

        lb_duration = Label(self, text="Duration")
        lb_duration.place(relx=0.1, rely=0.2, anchor=S)

        lb_duration_num = Label(self, text="45 minutes")
        lb_duration_num.place(relx=0.1, rely=0.25, anchor=S)

        lb_calories_brnt = Label(self, text="Calories Burnt")
        lb_calories_brnt.place(relx=0.1, rely=0.45, anchor=S)

        lb_calories_brnt_num = Label(self, text="320 calories")
        lb_calories_brnt_num.place(relx=0.1, rely=0.50, anchor=S)


        lb_workout_list = Label(self, text="Workouts")
        lb_workout_list.place(relx=0.1, rely=0.7, anchor=S)

        Workout1 = Button(self, text='test1', bg="gray70",
                           bd=3, pady=5, font=("Helvetica", Fsize), width=4)
        Workout1.place(relx=0.1, rely=0.8, anchor=S)

        Workout2 = Button(self, text='test1', bg="gray70",
                          bd=3, pady=5, font=("Helvetica", Fsize), width=4)
        Workout2.place(relx=0.2, rely=0.8, anchor=S)

        Workout3 = Button(self, text='test1', bg="gray70",
                          bd=3, pady=5, font=("Helvetica", Fsize), width=4)
        Workout3.place(relx=0.3, rely=0.8, anchor=S)

        vscrollbar = Scrollbar(self, orient=HORIZONTAL)
        vscrollbar.place(relx=0.5, rely=0.95, anchor=S, width=600)

        #to pass variables across class use find_page and make sure its tkinter variable and its called using self.variable

# Driver Code
# start()
app = tkinterApp()
app.mainloop()
