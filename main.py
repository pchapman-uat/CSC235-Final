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

def choices(choices, inputMsg):
    # TODO: Add index automaticly
    for choice in choices:
        print(choice)
    return intInput(inputMsg)

def addClass():
    name = input('Enter class display name (ie: Python I): ')
    id = input('Enter class ID (ie: CSC235): ')
    totalPoints = intInput('Enter total points: ')
    try:
        cursor.execute('INSERT INTO classes (id, name, totalPoints) VALUES (?,?, ?)', (id, name, totalPoints))
        # TODO: Add max score column
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
        print(f'{grade[0]}: {grade[1]} - {grade[2]}')
def getClasses():
    cursor.execute('SELECT id, totalPoints FROM classes')
    return cursor.fetchall()

def calculateGPA():
    # TODO: Option for only graded assignments
    choice = choices(["1. All", "2. Single"], "Please select a choice")
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
    GPAType = choices(["1. All assignments", "2. Only Graded"], "Please select the GPA type")
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
while True:
    choice = choices([
        '1. Add new class', 
        '2. View classes', 
        '3. Add a grade', 
        '4. View grades', 
        '5. Calculate GPA', 
        '0. Exit'], 
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
        calculateGPA()
        input()
    elif choice == 0:
        break