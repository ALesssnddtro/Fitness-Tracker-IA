from tkinter import *
import sqlite3
from tkinter import messagebox

root = Tk()
root.geometry("650x650")
root.title("app")

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
    if var_sessions_index.get() != 0:
        var_sessions_index.set(var_sessions_index.get() - 1)
        load_data()


def nav_right():
    if var_sessions_index.get() != var_sessions_length.get():
        var_sessions_index.set(var_sessions_index.get() + 1)
        load_data()


def add_session():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Sessions")
    data = c.fetchall()
    for i in range(var_sessions_length.get() + 1):
        if str(id_entry.get()) == str(data[i][0]):
            messagebox.showerror("Error", "That workout ID already exists")
        #else:
    insert(id_entry.get(), trained_entry.get(), burnt_entry.get(), reps_entry.get(), start_entry.get(), end_entry.get())




def remove_session():
    delete(id_entry.get())


def update_session():
    update(id_entry.get(), trained_entry.get(), burnt_entry.get(), reps_entry.get(), start_entry.get(), end_entry.get())


def clear_session():
    id_entry.delete(0, END)
    trained_entry.delete(0, END)
    burnt_entry.delete(0, END)
    reps_entry.delete(0, END)
    start_entry.delete(0, END)
    end_entry.delete(0, END)


# UI

# Left Arrow
left_btn = Button(text='<', width=3, command=nav_left)
left_btn.grid(row=3, column=1)

# Right Arrow
right_btn = Button(text='>', width=3, command=nav_right)
right_btn.grid(row=3, column=2)

# ID
id_text = StringVar()
id_label = Label(text='ID')
id_label.grid(row=0, column=0, sticky=E)
id_entry = Entry(textvariable=var_sessions_id)
id_entry.grid(row=0, column=1, sticky=E)

# MusclesTrained
trained_text = StringVar()
trained_label = Label(text='Muscles Trained')
trained_label.grid(row=0, column=2, sticky=E)
trained_entry = Entry(textvariable=var_sessions_trained)
trained_entry.grid(row=0, column=3, sticky=E)

# CaloriesBurnt
burnt_text = StringVar()
burnt_label = Label(text='Calories Burnt')
burnt_label.grid(row=1, column=0, sticky=E)
burnt_entry = Entry(textvariable=var_sessions_burnt)
burnt_entry.grid(row=1, column=1, sticky=E)

# Reps
reps_text = StringVar()
reps_label = Label(text='Reps')
reps_label.grid(row=1, column=2, sticky=E)
reps_entry = Entry(textvariable=var_sessions_reps)
reps_entry.grid(row=1, column=3, sticky=E)

# StartTime
start_text = StringVar()
start_label = Label(text='StartTime')
start_label.grid(row=2, column=0, sticky=E)
start_entry = Entry(textvariable=var_sessions_start)
start_entry.grid(row=2, column=1, sticky=E)

# EndTime
end_text = StringVar()
end_label = Label(text='EndTime')
end_label.grid(row=2, column=2, sticky=E)
end_entry = Entry(textvariable=var_sessions_end)
end_entry.grid(row=2, column=3, sticky=E)

add_btn = Button(text='Add Session', width=12, command=add_session)
add_btn.grid(row=4, column=0)

remove_btn = Button(text='Remove Session', width=12, command=remove_session)
remove_btn.grid(row=4, column=1)

update_btn = Button(text='Update Router', width=12, command=update_session)
update_btn.grid(row=4, column=2)

clear_btn = Button(text='Clear Input', width=12, command=clear_session)
clear_btn.grid(row=4, column=3)


def load_data():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Sessions")
    data = c.fetchall()
    row = data[var_sessions_index.get()]
    var_sessions_id.set(row[0])
    var_sessions_trained.set(row[1])
    var_sessions_burnt.set(row[2])
    var_sessions_reps.set(row[3])
    var_sessions_start.set(row[4])
    var_sessions_end.set(row[5])
    var_sessions_length.set(len(data) - 1)


# database
def insert(outID, trained, burnt, reps, start, end):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("INSERT INTO Sessions VALUES (?, ?, ?, ?, ?, ?)",
              (outID, trained, burnt, reps, start, end))
    conn.commit()


def delete(i):
    ans = messagebox.askquestion('Alert', 'Are you sure you sure?')
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    if ans == 'yes':
        c.execute("DELETE FROM Sessions WHERE WorkoutID=?", (i,))
    else:
        return
    conn.commit()


def update(WorkoutID, trained, burnt, reps, start, end):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute(
        "UPDATE Sessions SET MusclesTrained = ?, CaloriesBurnt = ?, Reps = ?, StartTime = ?, EndTime = ? WHERE WorkoutID = ?",
        (trained, burnt, reps, start, end, WorkoutID))
    conn.commit()


def fetch(id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Sessions WHERE WorkoutID = ?", (id,))
    rows = c.fetchall()
    return rows

#test
load_data()
root.mainloop()
