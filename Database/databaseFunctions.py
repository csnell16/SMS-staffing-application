import sqlite3
from enum import Enum, auto

class Notifications(Enum):
    ON = 0
    OFF = 1

class ShiftStatus(Enum):
    PENDING = auto()
    ASSIGNED = auto()
    CANCELLED = auto()

class BidStatus(Enum):
    PENDING = auto()
    ASSIGNED = auto()
    SHIFT_CANCELLED = auto()

class DistributionStatus(Enum):
    PENDING = auto()
    ASSIGNED  = auto()
    MANUALLY_PUSHED_BACK = auto()

class TableColumns(Enum):
    employeeID = auto()
    phone = auto()
    email = auto()
    notifications = auto()

    shiftID = auto()
    position = auto()
    startDateTime = auto()
    endDateTime = auto
    executionTime = auto()
    status = auto()
    assignee = auto()

    date = auto()

    bidStatus = auto()
    
    distributionOrder = auto()

class TableColumnsFull(Enum):
    FULL_EMPLOYEE = [TableColumns.employeeID.name, TableColumns.phone.name, TableColumns.email.name, TableColumns.notifications.name]
    FULL_SHIFT = [TableColumns.shiftID.name, TableColumns.position.name, TableColumns.startDateTime.name, TableColumns.endDateTime.name, TableColumns.executionTime.name, TableColumns.status.name, TableColumns.assignee.name]
    FULL_AVAILABILITY = [TableColumns.employeeID.name, TableColumns.date.name]
    FULL_BID = [TableColumns.employeeID.name, TableColumns.shiftID.name, TableColumns.bidStatus.name]

class FetchType(Enum):
    NONE = 0
    ONE = 1
    ALL = 2

class ItemNotFound(Exception):
    pass


DATABASE_FILE = './database.db'

def queryHelper(query, dataObj={}, fetchType=FetchType.NONE.value):
    # opens a db connection and executes a query
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    # enable foreign key support
    cursor.execute('PRAGMA foreign_keys = ON')
    connection.commit()

    # will still throw exceptions
    res = None
    if fetchType  == FetchType.ONE.value:
        res = cursor.execute(query, dataObj).fetchone()
    elif fetchType == FetchType.ALL.value:
        res = cursor.execute(query, dataObj).fetchall()
    else:
        cursor.execute(query, dataObj)
    connection.commit()

    cursor.close()
    connection.close()
    return res

def tupleToDict(tup, dictKeys):
    # turns a tuple into a dictionary with keys in the order given
    # tuple and keys list should have equal length
    dic = {}
    for i in range(len(tup)):
        dic[dictKeys[i]] = tup[i]
    return dic

def listTupleToDict(ls, dictKeys):
    # turns a list of tuples into a list of dictionaries with keys in the order given
    # tuple and keys list should have equal length
    return [tupleToDict(tup, dictKeys) for tup in ls]

def listTupleToValue(ls):
    # turns a list of tuples into a list of dictionaries with keys in the order given
    # tuple and keys list should have equal length
    return [tup[0] for tup in ls]

def initialize_tables():
    # intialize the tables if they have not already been created
    
    # Employees table
    queryHelper(f'''CREATE TABLE IF NOT EXISTS employees(
                employeeID TEXT PRIMARY KEY,
                phone TEXT,
                email TEXT,
                notifications INTEGER DEFAULT {Notifications.ON.value}
                )''')

    # Shifts table
    queryHelper(f'''CREATE TABLE IF NOT EXISTS shifts(
                shiftID INTEGER PRIMARY KEY AUTOINCREMENT,
                position TEXT,
                startDateTime TEXT,
                endDateTime TEXT,
                executionTime TEXT,
                status TEXT DEFAULT {ShiftStatus.PENDING.name},
                assignee TEXT DEFAULT NULL,
                FOREIGN KEY(assignee) REFERENCES employees(employeeID) ON UPDATE CASCADE
                )''')

    # Availability table
    queryHelper('''CREATE TABLE IF NOT EXISTS availability(
                employeeID TEXT NOT NULL,
                date TEXT,
                FOREIGN KEY(employeeID) REFERENCES employees(employeeID) ON UPDATE CASCADE,
                PRIMARY KEY (employeeID, date)
                )''')

    # Bids table
    queryHelper(f'''CREATE TABLE IF NOT EXISTS bids(
                employeeID TEXT NOT NULL,
                shiftID TEXT NOT NULL,
                bidStatus TEXT DEFAULT {BidStatus.PENDING.name},
                FOREIGN KEY(employeeID) REFERENCES employees(employeeID) ON UPDATE CASCADE,
                FOREIGN KEY(shiftID) REFERENCES shifts(shiftID) ON UPDATE CASCADE,
                PRIMARY KEY (employeeID, shiftID)
                )''')
    
    # Distribution table
    queryHelper(f'''CREATE TABLE IF NOT EXISTS distribution(
                employeeID TEXT NOT NULL,
                distOrder INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                distStatus TEXT DEFAULT {DistributionStatus.PENDING.name},
                FOREIGN KEY(employeeID) REFERENCES employees(employeeID) ON UPDATE CASCADE
                )''')
    
    # # Distribution table trigger
    queryHelper(f'''CREATE TRIGGER IF NOT EXISTS distTrigger
                AFTER INSERT ON employees
                BEGIN
                    INSERT INTO distribution (employeeID) VALUES (NEW.employeeID);
                END''')

# db insert functions
def insert_employee(employeeID, phone, email, notifications=Notifications.ON.value):
    queryHelper('INSERT INTO employees VALUES (?, ?, ?, ?)', (employeeID, phone, email, notifications))

def insert_shift(position, startDateTime, endDateTime, executionTime):
    queryHelper('INSERT INTO shifts (position, startDateTime, endDateTime, executionTime) VALUES (?, ?, ?, ?)', (position, startDateTime, endDateTime, executionTime))

def insert_availability(employeeID, date):
    queryHelper('INSERT INTO availability VALUES (?, ?)', (employeeID, date))

def insert_bid(employeeID, shiftID):
    queryHelper('INSERT INTO bids VALUES (?, ?)', (employeeID, shiftID))

# db update functions
def update_employee_employeeID(employeeID, newID):
    queryHelper('''UPDATE employees
                   SET employeeID = :newID
                   WHERE employeeID = :employeeID''',
                   {'employeeID': employeeID, 'newID': newID})

def update_employee_phone(employeeID, phone):
    queryHelper('''UPDATE employees
                   SET phone = :phone
                   WHERE employeeID = :employeeID''',
                   {'employeeID': employeeID, 'phone': phone})

def update_employee_email(employeeID, email):
    queryHelper('''UPDATE employees
                   SET email = :email
                   WHERE employeeID = :employeeID''',
                   {'employeeID': employeeID, 'email': email})

def update_employee_notifications(employeeID, notifications):
    queryHelper('''UPDATE employees
                   SET notifications = :notifications
                   WHERE employeeID = :employeeID''',
                   {'employeeID': employeeID, 'notifications': notifications})

def update_shift_status(shiftID, status):
    queryHelper('''UPDATE shifts
                   SET status = :status
                   WHERE shiftID = :shiftID''',
                   {'shiftID': shiftID, 'status': status})

def update_shift_assignee(shiftID, assignee):
    queryHelper('''UPDATE shifts
                   SET assignee = :assignee
                   WHERE shiftID = :shiftID''',
                   {'shiftID': shiftID, 'assignee': assignee})

def update_shift_assign_shift(shiftID, assignee):
    # updates assignee(employeeID) and status to assign
    queryHelper('''UPDATE shifts
                   SET assignee = :assignee, status = :status
                   WHERE shiftID = :shiftID''',
                   {'shiftID': shiftID, 'assignee': assignee, 'status': ShiftStatus.ASSIGNED.name})

def update_shift_cancel_shift(shiftID):
    # cancel shift and unassign it
    queryHelper('''UPDATE shifts
                   SET assignee = :assignee, status = :status
                   WHERE shiftID = :shiftID''',
                   {'shiftID': shiftID, 'assignee': None, 'status': ShiftStatus.CANCELLED.name})

# db delete functions
def delete_availability(employeeID, date):
    queryHelper('DELETE FROM availability WHERE employeeID = :employeeID AND date(date) = date(:date)',
                   {'employeeID': employeeID, 'date': date})

def delete_bid(employeeID, shiftID):
    queryHelper('DELETE FROM bids WHERE employeeID = :employeeID AND shiftID = :shiftID',
                   {'employeeID': employeeID, 'shiftID': shiftID})

# db read functions
def read_employee(employeeID):
    # get employee by ID
    res = queryHelper('SELECT * FROM employees WHERE employeeID = :employeeID',
                   {'employeeID': employeeID},
                   FetchType.ONE.value)
    if res is None:
        raise ItemNotFound
    return tupleToDict(res, TableColumnsFull.FULL_EMPLOYEE.value)

def read_employee_phone(employeeID):
    res = queryHelper('SELECT phone FROM employees WHERE employeeID = :employeeID',
                   {'employeeID': employeeID},
                   FetchType.ONE.value)
    if res is None:
        raise ItemNotFound
    return tupleToDict(res, [TableColumns.phone.name])

def read_employee_email(employeeID):
    res = queryHelper('SELECT email FROM employees WHERE employeeID = :employeeID',
                   {'employeeID': employeeID},
                   FetchType.ONE.value)
    if res is None:
        raise ItemNotFound
    return tupleToDict(res, [TableColumns.email.name])

def read_employee_notifications(employeeID):
    res = queryHelper('SELECT notifications FROM employees WHERE employeeID = :employeeID',
                   {'employeeID': employeeID},
                   FetchType.ONE.value)
    if res is None:
        raise ItemNotFound
    return tupleToDict(res, [TableColumns.notifications.name])

def read_shift(shiftID):
    # get shift by id
    res = queryHelper('SELECT * FROM shifts WHERE shiftID = :shiftID',
                   {'shiftID': shiftID},
                   FetchType.ONE.value)
    if res is None:
        raise ItemNotFound
    return tupleToDict(res, TableColumnsFull.FULL_SHIFT.value)

def read_shifts_by_assignee(assignee):
    # get all shifts by a specified assignee, assignee is null when unassigned
    res = queryHelper('SELECT * FROM shifts WHERE assignee IS :assignee',
                   {'assignee': assignee},
                   FetchType.ALL.value)
    return listTupleToDict(res, TableColumnsFull.FULL_SHIFT.value)

def read_shifts_unassigned():
    # get all shifts that are unassigned, regardless of status
    res = queryHelper('SELECT * FROM shifts WHERE assignee IS :assignee',
                   {'assignee': None},
                   FetchType.ALL.value)
    return listTupleToDict(res, TableColumnsFull.FULL_SHIFT.value)

def read_shifts_pending():
    # get all shifts with pending status
    res = queryHelper('SELECT * FROM shifts WHERE status IS :status',
                   {'status': ShiftStatus.PENDING.name},
                   FetchType.ALL.value)
    return listTupleToDict(res, TableColumnsFull.FULL_SHIFT.value)

def read_shifts_pending_past_execution():
    # get all pending shifts past execution time
    res = queryHelper('''SELECT * FROM shifts WHERE status IS :status
                         AND datetime(executionTime) <= datetime('now')''',
                         {'status': ShiftStatus.PENDING.name},
                         FetchType.ALL.value)
    return listTupleToDict(res, TableColumnsFull.FULL_SHIFT.value)

def read_shifts_assigned():
    # get all shifts with assigned status
    res = queryHelper('''SELECT * FROM shifts WHERE status IS :status''',
                         {'status': ShiftStatus.ASSIGNED.name},
                         FetchType.ALL.value)
    return listTupleToDict(res, TableColumnsFull.FULL_SHIFT.value)

def read_shifts_cancelled():
    # get all shifts with cancelled status
    res = queryHelper('''SELECT * FROM shifts WHERE status IS :status''',
                         {'status': ShiftStatus.CANCELLED.name},
                         FetchType.ALL.value)
    return listTupleToDict(res, TableColumnsFull.FULL_SHIFT.value)

def read_availability_by_employee_and_month(employeeID, month):
    # get an employees availability for a specified month 'yyyy-mm'
    res = queryHelper('''SELECT date FROM availability WHERE employeeID = :employeeID
                         AND strftime('%Y-%m', date) = :month
                         ORDER BY date ASC''',
                         {'employeeID': employeeID, 'month': month},
                         FetchType.ALL.value)
    return listTupleToValue(res)

def read_availability_by_day(day):
    # get all available employees on a specified day 'yyyy-mm-dd'
    res = queryHelper('''SELECT employeeID FROM availability WHERE
                         date(date) = :day''',
                         {'day': day},
                         FetchType.ALL.value)
    return listTupleToValue(res)

def read_bids_employees_by_shift(shiftID):
    # get all employeeIDs by the given shiftID in the bid table
    res = queryHelper('SELECT employeeID FROM bids WHERE shiftID IS :shiftID',
                   {'shiftID': shiftID},
                   FetchType.ALL.value)
    return listTupleToValue(res)

def read_bids_shifts_by_employee(employeeID):
    # get all shiftIDs by the given employeeID in the bid table
    res = queryHelper('SELECT shiftID FROM bids WHERE employeeID IS :employeeID',
                   {'employeeID': employeeID},
                   FetchType.ALL.value)
    return listTupleToValue(res)

initialize_tables()