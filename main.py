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
    for i in range(len(choices)):
        if "Exit" in choices[i]:
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
    cursor.execute('SELECT * FROM classes')
    classes = cursor.fetchall()
    allIds = []
    for class_ in classes:
        allIds.append(class_[0])
        print(f'{class_[0]}: {class_[1]} | Total Points: {class_[2]}')
    if len(allIds) == 0:
        colors.printYellowLine("No classes found")
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
        if maxScore != 0:
            print(class_[0]+":")
            if GPAType == 1:
                print("Total: ", total, "Of:", class_[1])
                print((total / class_[1]) * 4)
            else:
                print("Total: ", total, "Of:", maxScore,"*")
                print((total / maxScore) * 4)
        else: 
            print(class_[0]+":")
            print("No grades found")
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
    newName = input(f"Please enter the new Name (old: {grade[1]})")

    if newGrade == "":
        newGrade = grade[2]
    if newMaxGrade == "":
        newMaxGrade = grade[3]
    if newName == "":
        newName = grade[1]
    cmd = f"UPDATE {classID} SET grade={newGrade}, maxGrade={newMaxGrade}, name='{newName}' WHERE id={id}"
    cursor.execute(cmd)
    conn.commit()

def editClass():
    allIds = viewClasses()
    classID = input('Enter current class ID: ')
    while classID not in allIds: 
        classID = input(colors.genRedLine("Not a valid id, please try again"))
    old = cursor.execute(f'SELECT * FROM classes WHERE id="{classID}"').fetchone()
    name = input(f'Enter new class display name (old: {old[1]}): ')
    id = input(f'Enter new class ID (old: {old[0]}): ')
    totalPoints = intInput(f'Enter new total points (old: {old[2]}): ')
    try:
        cursor.execute(f'UPDATE classes SET id="{id}", name="{name}", totalPoints={totalPoints} WHERE id="{classID}"')
        conn.commit()
        colors.printGreenLine('Class edited')
    except any:
        colors.printRedLine("Failed to edit class")
colors.printBlueLine("\t\tGPA Calulator")
colors.printPurpleLine("\t     By: Preston Chapman")
colors.printRedLine("\t\tCSC235 | UAT")
print()

print("This application will allow you to store your grades, and calculate the GPA")
print("Select help for more infomation")

while True:
    choice = choices([
        colors.genGreenLine('Add new class'), 
        colors.genCyanLine('View classes'), 
        colors.genGreenLine('Add a grade'), 
        colors.genBlueLine('View grades'),
        colors.genYellowLine('Edit a grade or class'), 
        colors.genPurpleLine('Calculate GPA'),
        'Help',
        colors.genRedLine('Exit')], 
        'Enter your choice: ')

    if choice == 1:
        colors.printGreenLine("Adding new class")
        addClass()
    elif choice == 2:
        colors.printCyanLine("Viewing classes")
        viewClasses()
    elif choice == 3:
        colors.printGreenLine("Adding a grade")
        addGrade()
    elif choice == 4:
        colors.printBlueLine("Viewing grades")
        viewClasses()
        viewGrades()
    elif choice == 5:
        colors.printYellowLine("Editing a grade or class")
        choice = choices(["Grade", "Class"], "Please select a choice")
        if choice == 1:
            viewClasses()
            classID = viewGrades()
            editGrade(classID)
        else:
            editClass()
    elif choice == 6:
        colors.printPurpleLine("Calculating GPA")
        calculateGPA()
    elif choice == 7:
        print("Help")
        choice = choices([
        'Add new class', 
        'View classes', 
        'Add a grade', 
        'View grades',
        'Edit a grade or class', 
        'Calculate GPA',
        'Exit'], 
        'Enter your choice: ')
        if choice == 1:
            print("1. Add a class")
            print("This will add a class to the database")
            print("A class is needed to add a grade")
            print("Classes will accept a ID, Name, and max score")
        elif choice == 2:
            print("2. View Classes")
            print("This will display the following information")
            print("Class ID")
            print("Class Name")
            print("Max Score") 
        elif choice == 3:
            print("3. Add a grade")
            print("This will add a grade to the database")
            print("First you will select a class to add a grade for")
            print("Then you will add the grade you got on the asignemnt")
            print("Then the max score you can get on the assignment")
            print("Then the assignment name or number")
        elif choice == 4:
            print("4. View Grades")
            print("This will display all grades for a class")
            print("It will prompt you to enter a class by its ID")
            print('Then it will print the assignment ID, Name, score, and max score for every assignment')
        elif choice == 5:
            print('5. Edit a grade')
            print("This will allow you to edit an existing grade")
            print("It will prompt you to enter in a class ID")
            print('Then it will ask for the grade ID')
            print("Then you will input the new values")
            print("To keep the value the same push enter")
        elif choice == 6:
            print("6. Calculate GPA")
            print("This will calculate your GPA on a 4.0 scale")
            print("First you will select all classes or a singular class")
            print("Then you will chose to calculate all assignments, or only graded")
            print("Then it will print your GPA for the selcted class or for all classes")
    elif choice == 0:
        break
    print()