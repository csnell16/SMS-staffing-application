import sqlite3
from enum import Enum, auto

class Notifications(Enum):
    ON = 0
    OFF = 1

class ShiftStatus(Enum):
    PENDING = auto()
    ASSIGNED = auto()
    CANCELLED = auto()
    UNABLE_TO_ASSIGN = auto()

class BidStatus(Enum):
    PENDING = auto()
    ASSIGNED = auto()
    REJECTED = auto()
    SHIFT_CANCELLED = auto()

class DistributionStatus(Enum):
    PENDING = auto()
    ASSIGNED  = auto()
    MANUALLY_PUSHED_BACK = auto()
    AUTO_ASSIGNED = auto()
    FORCE_ASSIGNED = auto()
    OTHER = auto()

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
    
    distOrder = auto()
    distStatus = auto()

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
    try:
        res = None
        if fetchType  == FetchType.ONE.value:
            res = cursor.execute(query, dataObj).fetchone()
        elif fetchType == FetchType.ALL.value:
            res = cursor.execute(query, dataObj).fetchall()
        else:
            cursor.execute(query, dataObj)
        connection.commit()
    finally:
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
                shiftID TEXT DEFAULT NULL,
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
    res = queryHelper('''INSERT INTO shifts (position, startDateTime, endDateTime, executionTime) VALUES (?, ?, ?, ?) RETURNING  *''',
                      (position, startDateTime, endDateTime, executionTime),
                      FetchType.ONE.value)
    return tupleToDict(res, TableColumnsFull.FULL_SHIFT.value)

def insert_availability(employeeID, date):
    queryHelper('INSERT INTO availability VALUES (?, ?)', (employeeID, date))

def insert_bid(employeeID, shiftID):
    queryHelper('INSERT INTO bids (employeeID, shiftID) VALUES (?, ?)', (employeeID, shiftID))

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

def update_shift_assign_shift(shiftID, assignee, assignmentType=DistributionStatus.ASSIGNED.name):
    # updates assignee(employeeID) and status to assign
    queryHelper('''UPDATE shifts
                   SET assignee = :assignee, status = :status
                   WHERE shiftID = :shiftID''',
                   {'shiftID': shiftID, 'assignee': assignee, 'status': ShiftStatus.ASSIGNED.name})
    # update bids
    update_bids_winner(shiftID, assignee)
    # update distribution
    update_distribution_assign_reinsert(assignee, assignmentType, shiftID)

def update_shift_cancel_shift(shiftID):
    # cancel shift and unassign it
    queryHelper('''UPDATE shifts
                   SET assignee = :assignee, status = :status
                   WHERE shiftID = :shiftID''',
                   {'shiftID': shiftID, 'assignee': None, 'status': ShiftStatus.CANCELLED.name})
    # cancel bid status for related bids
    update_bids_cancelled_shift(shiftID)

def update_bids_winner(shiftID, winnerEmployeeID):
    # updates bids such that the bid winner gets accepted and the rest are rejected
    queryHelper('''UPDATE bids
                   SET bidStatus =
                        CASE WHEN employeeID = :winnerEmployeeID
                            THEN :bidWin
                            ELSE :bidLose
                        END
                   WHERE shiftID = :shiftID''',
                   {'shiftID': shiftID, 'winnerEmployeeID': winnerEmployeeID, 'bidWin': BidStatus.ASSIGNED.name, 'bidLose': BidStatus.REJECTED.name})

def update_bids_cancelled_shift(shiftID):
    # set bid status to cancelled for related bids
    queryHelper('''UPDATE bids
                   SET bidStatus = :bidStatus
                   WHERE shiftID = :shiftID''',
                   {'shiftID': shiftID, 'bidStatus': BidStatus.SHIFT_CANCELLED.name})

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

def read_employees_by_phone(phone):
    # get all employeeIDs associated to given phone number
    res = queryHelper('SELECT employeeID FROM employees WHERE phone = :phone',
                   {'phone': phone},
                   FetchType.ALL.value)
    return listTupleToValue(res)

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

def read_availability_phone_by_day(day):
    # get all phone numbers of employees that are available on the specified day 'yyyy-mm-dd'
    res = queryHelper('''SELECT employees.employeeID, notifications, phone
                      FROM employees
                      JOIN availability
                      ON employees.employeeID = availability.employeeID AND date(availability.date) = :day''',
                         {'day': day},
                         FetchType.ALL.value)
    return listTupleToDict(res, [TableColumns.employeeID.name, TableColumns.notifications.name, TableColumns.phone.name])

def read_bids_employees_by_shift(shiftID):
    # get all employeeIDs by the given shiftID in the bid table
    res = queryHelper('SELECT employeeID FROM bids WHERE shiftID IS :shiftID',
                   {'shiftID': shiftID},
                   FetchType.ALL.value)
    return listTupleToValue(res)

def read_bids_employees_phone_by_shift(shiftID):
    # get all IDs, notification settings, phone numbers, and the bid status of all employees for the given shiftID
    res = queryHelper('''SELECT employees.employeeID, notifications, phone, bidStatus
                      FROM employees
                      JOIN bids
                      ON employees.employeeID = bids.employeeID AND bids.shiftID = :shiftID''',
                         {'shiftID': shiftID},
                         FetchType.ALL.value)
    return listTupleToDict(res, [TableColumns.employeeID.name, TableColumns.notifications.name, TableColumns.phone.name, TableColumns.bidStatus.name])

def read_bids_shifts_by_employee(employeeID):
    # get all shiftIDs by the given employeeID in the bid table
    res = queryHelper('SELECT shiftID FROM bids WHERE employeeID IS :employeeID',
                   {'employeeID': employeeID},
                   FetchType.ALL.value)
    return listTupleToValue(res)

# db special/scheduling functions
def update_distribution_assign_reinsert(employeeID, assignmentType, shiftID=None):
    # validate distribution status
    if assignmentType not in DistributionStatus.__members__.keys():
        assignmentType = DistributionStatus.OTHER.name
    # update previous distribution status for assignee
    queryHelper('''UPDATE distribution
                   SET distStatus = :distStatus, shiftID = :shiftID
                   WHERE employeeID = :employeeID AND distStatus = :pending''',
                   {'shiftID': shiftID, 'employeeID': employeeID, 'distStatus': assignmentType, 'pending': DistributionStatus.PENDING.name})
    # re-insert assignee into distribution to put on back of list
    queryHelper('INSERT INTO distribution (employeeID) VALUES (?)', (employeeID,))

def read_distribution_by_shift_pending_bids(shiftID):
    # gets the distribution list by the distribution order and filters by employees that have placed a bid
    res = queryHelper('''SELECT distribution.employeeID
                      FROM distribution
                      RIGHT JOIN bids
                      ON distribution.employeeID = bids.employeeID
                      WHERE bids.shiftID = :shiftID
                      AND distStatus = :distStatus
                      ORDER BY distOrder ASC
                      ''',
                   {'shiftID': shiftID,'distStatus': DistributionStatus.PENDING.name},
                   FetchType.ALL.value)
    return listTupleToValue(res)

def read_distribution_by_availability_date(date):
    # gets the distribution list by the distribution order and filters by employees that have availability that date 'yyyy-mm-dd' or iso datetime
    res = queryHelper('''SELECT distribution.employeeID
                      FROM distribution
                      RIGHT JOIN availability
                      ON distribution.employeeID = availability.employeeID
                      WHERE date(availability.date) = date(:date)
                      AND distStatus = :distStatus
                      ORDER BY distOrder ASC
                      ''',
                   {'date': date,'distStatus': DistributionStatus.PENDING.name},
                   FetchType.ALL.value)
    return listTupleToValue(res)

def update_shift_auto_assign(shiftID, forceAssign=False):
    # automatically process for assigning a shift based on the distribution list
    # force assign allows employees available on shift day to be selected after bidders

    shift = read_shift(shiftID)

    # if shift is already assigned, return the assigned employeeID
    if shift[TableColumns.status.name] == ShiftStatus.ASSIGNED.name:
        return read_employee(shift[TableColumns.assignee.name])

    # if shift was cancelled, return null
    if shift[TableColumns.status.name] == ShiftStatus.CANCELLED.name:
        return None

    # if shift was previously marked unassignable by the auto-assigner, pass to try assigning again
    if shift[TableColumns.status.name] == ShiftStatus.UNABLE_TO_ASSIGN.name:
        pass

    # first get distribution by pending bids
    dist = read_distribution_by_shift_pending_bids(shiftID)

    # if there are bids, assign to the first in the list
    if len(dist) > 0:
        assignee = dist[0]
        # update shift, bidlist and distribution
        update_shift_assign_shift(shiftID, assignee, DistributionStatus.AUTO_ASSIGNED.name)
        return read_employee(assignee)

    # if there were no bids to assign from then check forceAssign
    if not forceAssign:
        # when force assign is False, mark shift as 'unable to assign' and end without assigning
        update_shift_status(shiftID, ShiftStatus.UNABLE_TO_ASSIGN.name)
        return None

    # When forceAssign is True, assign to the first in the distribution list that is available that day
    dist = read_distribution_by_availability_date(shift[TableColumns.startDateTime.name])

    # if there are employees available that date, assign to the first available in the distribution list
    if len(dist) > 0:
        assignee = dist[0]
        # update shift, bidlist and distribution
        update_shift_assign_shift(shiftID, assignee, DistributionStatus.FORCE_ASSIGNED.name)
        return read_employee(assignee)

    # if no one is available that date, mark as unable to assign
    update_shift_status(shiftID, ShiftStatus.UNABLE_TO_ASSIGN.name)
    return None

# initialization calls
initialize_tables()