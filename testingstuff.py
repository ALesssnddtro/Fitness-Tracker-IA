import sqlite3
from datetime import datetime
from datetime import timedelta

def ReminderCheck():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM Sessions'):

        duration = row[4]
        d1 = datetime.today()
        CurrentTime = d1.strftime("%Y-%m-%d %I:%M:%S %p")
        print(CurrentTime)
        CurrentTime = str(CurrentTime)
        print(CurrentTime)
        CurrentTime = datetime.strptime(CurrentTime, "%Y-%m-%d %H:%M:%S %p")
        print(CurrentTime)
        date_str = row[2] + " " + row[3]

        minStart = datetime.strptime(date_str, "%Y-%m-%d %I:%M:%S")


        maxStart = minStart + timedelta(minutes=duration)

        #print(CurrentTime, "-", minStart, "-", maxStart)

        if CurrentTime >= minStart and CurrentTime < maxStart:
            print("day is the day")

def test():
    canvas = Canvas()
    scroll_y = Scrollbar(, orient="vertical", command=frame)

    frame = Frame(canvas)
    # group of widgets
    for i in range(20):
        tk.Label(frame, text='label %i' % i).pack()
    # put the frame in the canvas
    canvas.create_window(0, 0, anchor='nw', window=frame)
    # make sure everything is displayed before configuring the scrollregion
    canvas.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox('all'),
                     yscrollcommand=scroll_y.set)

    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')
test()

