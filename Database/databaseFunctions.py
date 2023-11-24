import sqlite3

DATABASE_FILE = './database.db'

connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()

# enable foreign key support
cursor.execute('PRAGMA foreign_keys = ON')
connection.commit()

def initialize_tables():
    # intialize the tables if they have not already been created
    
    # Employees table
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees(
                employeeID TEXT PRIMARY KEY,
                phone TEXT,
                email TEXT,
                notifications INTEGER DEFAULT 0
                )''')

    # Shifts table
    cursor.execute('''CREATE TABLE IF NOT EXISTS shifts(
                shiftID INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                executionTime TEXT,
                status INTEGER DEFAULT 0,
                assignee TEXT DEFAULT NULL,
                FOREIGN KEY(assignee) REFERENCES employees(employeeID) ON UPDATE CASCADE
                )''')

    # Availability table
    cursor.execute('''CREATE TABLE IF NOT EXISTS availability(
                employeeID TEXT NOT NULL,
                date TEXT,
                FOREIGN KEY(employeeID) REFERENCES employees(employeeID) ON UPDATE CASCADE,
                PRIMARY KEY (employeeID, date)
                )''')
    connection.commit()

# db insert functions
def insert_employee(employeeID, phone, email, notifications=0):
    cursor.execute('INSERT OR IGNORE INTO employees VALUES (?, ?, ?, ?)', (employeeID, phone, email, notifications))
    connection.commit()

def insert_shift(date, time, executionTime):
    cursor.execute('''INSERT INTO shifts
                   (date, time, executionTime)
                   VALUES (?, ?, ?)''',
                   (date, time, executionTime))
    connection.commit()

def insert_availability(employeeID, date):
    cursor.execute('INSERT OR IGNORE INTO availability VALUES (?, ?)', (employeeID, date))
    connection.commit()

# db update functions
def update_employee_employeeID(employeeID, newID):
    cursor.execute('''UPDATE employees
                   SET employeeID = :newID
                   WHERE employeeID = :employeeID''',
                   {'employeeID': employeeID, 'newID': newID})
    connection.commit()

def update_employee_phone(employeeID, phone):
    cursor.execute('''UPDATE employees
                   SET phone = :phone
                   WHERE employeeID = :employeeID''',
                   {'employeeID': employeeID, 'phone': phone})
    connection.commit()

def update_employee_email(employeeID, email):
    cursor.execute('''UPDATE employees
                   SET email = :email
                   WHERE employeeID = :employeeID''',
                   {'employeeID': employeeID, 'email': email})
    connection.commit()

def update_employee_notifications(employeeID, notifications):
    cursor.execute('''UPDATE employees
                   SET notifications = :notifications
                   WHERE employeeID = :employeeID''',
                   {'employeeID': employeeID, 'notifications': notifications})
    connection.commit()

def update_shift_status(shiftID, status):
    cursor.execute('''UPDATE shifts
                   SET status = :status
                   WHERE shiftID = :shiftID''',
                   {'shiftID': shiftID, 'status': status})
    connection.commit()

def update_shift_assignee(shiftID, assignee):
    cursor.execute('''UPDATE shifts
                   SET assignee = :assignee
                   WHERE shiftID = :shiftID''',
                   {'shiftID': shiftID, 'assignee': assignee})
    connection.commit()

def update_shift_assign_shift(shiftID, assignee, status=1):
    cursor.execute('''UPDATE shifts
                   SET assignee = :assignee, status = :status
                   WHERE shiftID = :shiftID''',
                   {'shiftID': shiftID, 'assignee': assignee, 'status': status})
    connection.commit()

# db delete functions
def delete_availability(employeeID, date):
    cursor.execute('DELETE FROM availability WHERE employeeID = :employeeID AND date = :date',
                   {'employeeID': employeeID, 'date': date})
    connection.commit()

initialize_tables()

connection.close()