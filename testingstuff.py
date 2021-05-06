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

        print(CurrentDate, ExpectedDateMin, ExpectedDateMax)

        if CurrentDate > ExpectedDateMin and CurrentDate < ExpectedDateMax:
            print("within")
        else:
            print("without")

test()

