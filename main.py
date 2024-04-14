import sqlite3 
from colors import colors

conn = sqlite3.connect('db/grades.sqlite3')

cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS classes (id TEXT PRIMARY KEY, name TEXT)')

def intInput(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            colors.printRedLine('Invalid input, try again.')

def choices(choices, inputMsg):
    for choice in choices:
        print(choice)
    return intInput(inputMsg)

def addClass():
    name = input('Enter class name: ')
    id = input('Enter class ID: ')
    try:
        cursor.execute('INSERT INTO classes (id, name) VALUES (?,?)', (id, name))
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {id} (id INT PRIMARY KEY, name TEXT, grade INT)')
        conn.commit()
    except sqlite3.IntegrityError:
        colors.printRedLine('Class already exists')

def viewClasses():
    cursor.execute('SELECT * FROM classes')
    classes = cursor.fetchall()
    for class_ in classes:
        print(f'{class_[0]}: {class_[1]}')

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
        # TODO: Add a new class
        addClass()
    
    elif choice == 2:
        # TODO: View classes
        viewClasses()
    elif choice == 3:
        # TODO: Add grade
        print('Enter class name')
    elif choice == 4:
        # TODO: View grades
        print('Grades')
    elif choice == 5:
        # TODO: Calculate GPA
        print('GPA')
    elif choice == 0:
        break