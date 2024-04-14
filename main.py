import sqlite3 

conn = sqlite3.connect('example.db')
cursor = conn.cursor()
def intInput(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print('Please enter a number')

def choices(choices, inputMsg):
    for choice in choice:
        print(choice)
    return intInput(inputMsg)

while True:
    choice = choices([
        '1. Add new class', 
        '2. View classes', 
        '3. Add a grade', 
        '4. View grades', 
        '5. Calculate GPA', 
        '0. Exit'], 
        'Enter your choice: ')
    choice = int(input('Enter your choice: '))

    if choice == 1:
        # TODO: Add a new class
        print('Enter class name')
    elif choice == 2:
        # TODO: View classes
        print('Classes')
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