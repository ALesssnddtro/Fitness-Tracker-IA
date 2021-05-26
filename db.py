import sqlite3
conn = sqlite3.connect('library.db')
c = conn.cursor()
conn.execute("PRAGMA foreign_keys = 1")


# Create table
c.execute('''CREATE TABLE User
             (UserID int PRIMARY KEY,
             LastName text,
             FirstName text, 
             DoB text, 
             Weight int,
             TargetWeight int, 
             Height int,
             Reminders int,
             Gender text)''')

c.execute('''CREATE TABLE Sessions
             (SessionID int PRIMARY KEY,
             UserID time,
             StartDate date,
             StartTime time,
             Duration int,
             Place text,
             IsPlanned text,
             FOREIGN KEY (UserID) REFERENCES User(UserID))''')

#text 0 is false 1 is true
c.execute('''CREATE TABLE SessionDetails
             (SessionDetailsID int PRIMARY KEY,
             SessionID int,
             ExerciseID int,
             Sets int,
             Reps int,
             FOREIGN KEY (SessionID) REFERENCES Sessions(SessionID),
             FOREIGN KEY (ExerciseID) REFERENCES Exercises(ExerciseID))''')

c.execute('''CREATE TABLE Exercises
             (ExerciseID int PRIMARY KEY,
             ExerciseName text,
             Type text,
             CaloriesBurntPerRep)''')

#users
c.execute('''INSERT INTO User(UserID, LastName, FirstName, DoB, Weight, TargetWeight, Height, Gender, Reminders) 
VALUES (1, 'Davila', 'Nancy', '2003/01/02', 56, 52, 126, 'Female', 1)''')

#sessions
c.execute('''INSERT INTO Sessions(SessionID, UserID, StartDate, StartTime, Duration, Place, IsPlanned)
VALUES (1, 1, "2018/05/26", "06:55", 5, "Home", "True")''')
c.execute('''INSERT INTO Sessions(SessionID, UserID, StartDate, StartTime, Duration, Place, IsPlanned)
VALUES (2, 1, "2016/11/11", "02:45", 15, "Home", "True")''')

c.execute('''INSERT INTO Sessions(SessionID, UserID, StartDate, StartTime, Duration, Place, IsPlanned)
VALUES (3, 1, "2016/11/11", "02:35", 25, "Home", "True")''')
c.execute('''INSERT INTO Sessions(SessionID, UserID, StartDate, StartTime, Duration, Place, IsPlanned)
VALUES (4, 1, "2016/11/11", "04:25", 35, "Home", "True")''')

c.execute('''INSERT INTO Sessions(SessionID, UserID, StartDate, StartTime, Duration, Place, IsPlanned)
VALUES (5, 1, "2021/05/06", "11:15", 45, "Gym", "True")''')


#exercises
c.execute('''INSERT INTO Exercises(ExerciseID, ExerciseName, Type, CaloriesBurntPerRep)
VALUES (1, "Incline Bench", "Push-day", 4.4)''')

c.execute('''INSERT INTO Exercises(ExerciseID, ExerciseName, Type, CaloriesBurntPerRep)
VALUES (2, "Pullovers", "Pull-day", 3.3)''')

c.execute('''INSERT INTO Exercises(ExerciseID, ExerciseName, Type, CaloriesBurntPerRep)
VALUES (3, "Squats", "Leg-day", 5.5)''')

c.execute('''INSERT INTO Exercises(ExerciseID, ExerciseName, Type, CaloriesBurntPerRep)
VALUES (4, "Hammer Curl", "Pull-day", 2.2)''')

c.execute('''INSERT INTO Exercises(ExerciseID, ExerciseName, Type, CaloriesBurntPerRep)
VALUES (5, "DB Shrugs", "Pull-day", 1.3)''')

c.execute('''INSERT INTO Exercises(ExerciseID, ExerciseName, Type, CaloriesBurntPerRep)
VALUES (6, "Dumbbell rows", "Pull-day", 1.5)''')

#sessiondetails
c.execute('''INSERT INTO SessionDetails(SessionDetailsID, SessionID, ExerciseID, Sets, Reps)
VALUES (1, 2, 3, 3, 12)''')

c.execute('''INSERT INTO SessionDetails(SessionDetailsID, SessionID, ExerciseID, Sets, Reps)
VALUES (2, 3, 1, 4, 10)''')

c.execute('''INSERT INTO SessionDetails(SessionDetailsID, SessionID, ExerciseID, Sets, Reps)
VALUES (3, 1, 2, 2, 8)''')

c.execute('''INSERT INTO SessionDetails(SessionDetailsID, SessionID, ExerciseID, Sets, Reps)
VALUES (4, 4, 3, 3, 12)''')

c.execute('''INSERT INTO SessionDetails(SessionDetailsID, SessionID, ExerciseID, Sets, Reps)
VALUES (5, 5, 1, 4, 10)''')

c.execute('''INSERT INTO SessionDetails(SessionDetailsID, SessionID, ExerciseID, Sets, Reps)
VALUES (6, 5, 2, 3, 8)''')





conn.commit()
