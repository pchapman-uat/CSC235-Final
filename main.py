import sqlite3 
from colors import colors

conn = sqlite3.connect('db/grades.sqlite3')

cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS classes (id TEXT PRIMARY KEY, name TEXT, totalPoints INTEGER)')

def intInput(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            colors.printRedLine('Invalid input, try again.')

def intBlankInput(message):
    while True:
        resonse = input(message)
        try:
            return int(resonse)
        except ValueError:
            if resonse == "":
                return resonse
            else:
                colors.printRedLine('Invalid input, try again.')

def choices(choices, inputMsg):
    # TODO: Add index automaticly
    for i in range(len(choices)):
        if choices[i] == "Exit":
            print(f"0.", choices[i])
        else:
            print(f"{i+1}.", choices[i])
    return intInput(inputMsg)

def addClass():
    name = input('Enter class display name (ie: Python I): ')
    id = input('Enter class ID (ie: CSC235): ')
    totalPoints = intInput('Enter total points: ')
    try:
        cursor.execute('INSERT INTO classes (id, name, totalPoints) VALUES (?,?, ?)', (id, name, totalPoints))
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {id} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, grade INTEGER, maxGrade INTEGER)')
        conn.commit()
        colors.printGreenLine('Class added')
    except sqlite3.IntegrityError:
        colors.printRedLine('Class already exists')

def viewClasses():
    # TOOD: Display if there are no classes
    cursor.execute('SELECT * FROM classes')
    classes = cursor.fetchall()
    allIds = []
    for class_ in classes:
        allIds.append(class_[0])
        print(f'{class_[0]}: {class_[1]}')
    return allIds

def addGrade():
    allIds = viewClasses()
    id = input('Enter class ID: ')
    while id not in allIds: 
        id = input(colors.genRedLine("Not a valid id, please try again"))
    grade = intInput('Enter grade: ')
    maxGrade = intInput("Enter the max score: ")
    name = input('Enter assignment name: ')
    cursor.execute(f'INSERT INTO {id} (name, grade, maxGrade) VALUES (?,?,?)', (name, grade, maxGrade))
    conn.commit()

def viewGrades():
    id = input('Enter class ID: ')
    cursor.execute(f'SELECT * FROM {id}')
    grades = cursor.fetchall()
    if len(grades) == 0:
        colors.printYellowLine("No grades found")
    for grade in grades:
        print(f'{grade[0]}: {grade[1]} - {grade[2]}/{grade[3]}')
    return id
def getClasses():
    cursor.execute('SELECT id, totalPoints FROM classes')
    return cursor.fetchall()

def calculateGPA():
    # TODO: Option for only graded assignments
    choice = choices(["All", "Single"], "Please select a choice")
    classes = []
    if choice == 1: 
        classes = getClasses()
    else: 
        allids = viewClasses()
        id = input('Enter class ID: ')
        while id not in allids:
            id = input(colors.genRedLine("Not a valid class"))
        cursor.execute(f"SELECT id, totalPoints FROM classes WHERE id = '{id}'")
        classes = cursor.fetchall()
    GPAType = choices(["All assignments", "Only Graded"], "Please select the GPA type")
    for class_ in classes:
        cursor.execute(f'SELECT grade, maxGrade FROM {class_[0]}')
        grades = cursor.fetchall()
        total = 0
        maxScore = 0
        for grade in grades:
            total += grade[0]
            maxScore += grade[1]
        print(class_[0]+":")
        if GPAType == 1:
            print("Total: ", total, "Of:", class_[1])
            print((total / class_[1]) * 4)
        else:
            print("Total: ", total, "Of:", maxScore,"*")
            print((total / maxScore) * 4)
def getGrade(gradeID, classID):
    cursor.execute(f"SELECT * FROM {classID} WHERE id={gradeID}")
    grade = cursor.fetchone()
    return grade

def editGrade(classID):
    id = intInput("Please enter the grade ID")
    grade = getGrade(id, classID)

    print("Selected Assignment")
    print(grade[1])
    print(f"Grade: {grade[2]}/{grade[3]}")
    newGrade = intBlankInput(f"Please enter the new grade (old: {grade[2]})")
    newMaxGrade = intBlankInput(f"Please enter the new max grade (old: {grade[3]})")
    newName = intBlankInput(f"Please enter the new Name (old: {grade[1]})")

    if newGrade == "":
        newGrade = grade[2]
    if newMaxGrade == "":
        newMaxGrade = grade[3]
    if newName == "":
        newName = grade[1]
    cmd = f"UPDATE {classID} SET grade={newGrade}, maxGrade={newMaxGrade}, name='{newName}' WHERE id={id}"
    cursor.execute(cmd)
    conn.commit()

while True:
    choice = choices([
        'Add new class', 
        'View classes', 
        'Add a grade', 
        'View grades',
        'Edit a grade', 
        'Calculate GPA', 
        'Exit'], 
        'Enter your choice: ')

    if choice == 1:
        addClass()
        input()
    elif choice == 2:
        viewClasses()
        input()
    elif choice == 3:
        addGrade()
        input()
    elif choice == 4:
        viewClasses()
        viewGrades()
        input()
    elif choice == 5:
        viewClasses()
        classID = viewGrades()
        editGrade(classID)
    elif choice == 6:
        calculateGPA()
        input()
    elif choice == 0:
        break
