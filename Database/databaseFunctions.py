import sqlite3
from enum import Enum

class Notifications(Enum):
    ON = 0
    OFF = 1

class ShiftStatus(Enum):
    PENDING = 0
    ASSIGNED = 1

DATABASE_FILE = './database.db'

connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()

# enable foreign key support
cursor.execute('PRAGMA foreign_keys = ON')
connection.commit()

def initialize_tables():
    # intialize the tables if they have not already been created
    
    # Employees table
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS employees(
                employeeID TEXT PRIMARY KEY,
                phone TEXT,
                email TEXT,
                notifications INTEGER DEFAULT {Notifications.ON.value}
                )''')

    # Shifts table
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS shifts(
                shiftID INTEGER PRIMARY KEY AUTOINCREMENT,
                shiftDateTime TEXT,
                executionTime TEXT,
                status INTEGER DEFAULT {ShiftStatus.PENDING.value},
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

    # Bids table
    cursor.execute('''CREATE TABLE IF NOT EXISTS bids(
                employeeID TEXT NOT NULL,
                shiftID TEXT NOT NULL,
                FOREIGN KEY(employeeID) REFERENCES employees(employeeID) ON UPDATE CASCADE,
                FOREIGN KEY(shiftID) REFERENCES shifts(shiftID) ON UPDATE CASCADE,
                PRIMARY KEY (employeeID, shiftID)
                )''')
    
    connection.commit()

# db insert functions
def insert_employee(employeeID, phone, email, notifications=0):
    cursor.execute('INSERT OR IGNORE INTO employees VALUES (?, ?, ?, ?)', (employeeID, phone, email, notifications))
    connection.commit()

def insert_shift(shiftDateTime, executionTime):
    cursor.execute('INSERT INTO shifts (shiftDateTime, executionTime) VALUES (?, ?)', (shiftDateTime, executionTime))
    connection.commit()

def insert_availability(employeeID, date):
    cursor.execute('INSERT OR IGNORE INTO availability VALUES (?, ?)', (employeeID, date))
    connection.commit()

def insert_bid(employeeID, shiftID):
    cursor.execute('INSERT OR IGNORE INTO bids VALUES (?, ?)', (employeeID, shiftID))
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

def delete_bid(employeeID, shiftID):
    cursor.execute('DELETE FROM bids WHERE employeeID = :employeeID AND shiftID = :shiftID',
                   {'employeeID': employeeID, 'shiftID': shiftID})
    connection.commit()

# db read functions
def read_employee(employeeID):
    # get employee by ID
    res = cursor.execute('SELECT * FROM employees WHERE employeeID = :employeeID',
                   {'employeeID': employeeID})
    connection.commit()
    return res.fetchone()

def read_employee_phone(employeeID):
    res = cursor.execute('SELECT phone FROM employees WHERE employeeID = :employeeID',
                   {'employeeID': employeeID})
    connection.commit()
    return res.fetchone()

def read_employee_email(employeeID):
    res = cursor.execute('SELECT email FROM employees WHERE employeeID = :employeeID',
                   {'employeeID': employeeID})
    connection.commit()
    return res.fetchone()

def read_employee_notifications(employeeID):
    res = cursor.execute('SELECT notifications FROM employees WHERE employeeID = :employeeID',
                   {'employeeID': employeeID})
    connection.commit()
    return res.fetchone()

def read_shift(shiftID):
    # get shift by id
    res = cursor.execute('SELECT * FROM shifts WHERE shiftID = :shiftID',
                   {'shiftID': shiftID})
    connection.commit()
    return res.fetchone()

def read_shifts_by_assignee(assignee):
    # get all shifts by a specified assignee, assignee is null when unassigned
    res = cursor.execute('SELECT * FROM shifts WHERE assignee IS :assignee',
                   {'assignee': assignee})
    connection.commit()
    return res.fetchall()

def read_shifts_unassigned():
    # get all shifts that are unassigned, regardless of status
    res = cursor.execute('SELECT * FROM shifts WHERE assignee IS :assignee',
                   {'assignee': None})
    connection.commit()
    return res.fetchall()

def read_pending_shifts():
    # get all shifts with pending status
    res = cursor.execute('SELECT * FROM shifts WHERE status IS :status',
                   {'status': ShiftStatus.PENDING.value})
    connection.commit()
    return res.fetchall()

def read_shifts_pending_past_execution():
    # get all pending shifts past execution time
    res = cursor.execute('''SELECT * FROM shifts WHERE status IS :status
                         AND datetime(executionTime) <= datetime('now')''',
                         {'status': ShiftStatus.PENDING.value})
    connection.commit()
    return res.fetchall()

def read_availability_by_employee_and_month(employeeID, month):
    # get an employees availability for a specified month 'yyyy-mm'
    res = cursor.execute('''SELECT * FROM availability WHERE employeeID = :employeeID
                         AND strftime('%Y-%m', date) = :month''',
                         {'employeeID': employeeID, 'month': month})
    connection.commit()
    return res.fetchall()

def read_availability_by_day(day):
    # get all available employees on a specified day 'yyyy-mm-dd'
    res = cursor.execute('''SELECT * FROM availability WHERE
                         date(date) = :day''',
                         {'day': day})
    connection.commit()
    return res.fetchall()

def read_bids_employees_by_shift(shiftID):
    # get all employeeIDs by the given shiftID in the bid table
    res = cursor.execute('SELECT employeeID FROM bids WHERE shiftID IS :shiftID',
                   {'shiftID': shiftID})
    connection.commit()
    return res.fetchall()

def read_bids_shifts_by_employee(employeeID):
    # get all shiftIDs by the given employeeID in the bid table
    res = cursor.execute('SELECT shiftID FROM bids WHERE employeeID IS :employeeID',
                   {'employeeID': employeeID})
    connection.commit()
    return res.fetchall()

initialize_tables()

# Do NOT close database, database connection is still run while being imported in the API
# create database class to manage connections and refactor this behavior later
# connection.close()