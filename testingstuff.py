import sqlite3
from datetime import datetime
from datetime import timedelta

def ReminderCheck():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM Sessions'):

        duration = row[4]
        d1 = datetime.today()
        CurrentTime = d1.strftime("%Y-%m-%d %I:%M:%S")
        CurrentTime = str(CurrentTime)
        CurrentTime = datetime.strptime(CurrentTime, "%Y-%m-%d %I:%M:%S")

        date_str = row[2] + " " + row[3]

        minStart = datetime.strptime(date_str, "%Y-%m-%d %I:%M:%S")


        maxStart = minStart + timedelta(minutes=duration)

        print(type(date_str), CurrentTime, "-", minStart, "-", maxStart)
        print(type(d1), type(CurrentTime), "-", type(minStart), "-", type(maxStart))

        if CurrentTime >= minStart and CurrentTime < maxStart:
            print("day is the day")


ReminderCheck()

