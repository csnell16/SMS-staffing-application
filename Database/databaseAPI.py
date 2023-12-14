from flask import Flask, request, make_response
from sqlite3 import IntegrityError
import databaseFunctions as dbF
from databaseFunctions import ItemNotFound

app = Flask(__name__)

@app.route("/employees", methods=['POST'])
def create_employee():
    try:
        data = request.get_json()

        employeeID = data['employeeID']
        phone = data['phone']
        email = data['email']
        
        if 'notifications' in data:
            notifications = data['notifications']
            dbF.insert_employee(employeeID, phone, email, notifications)
        else:
            dbF.insert_employee(employeeID, phone, email)

        res = make_response('Successfully created employee')
        res.status_code = 201
    except KeyError:
        res = make_response('Request requires employeeID, phone, email, (optional) notifications')
        res.status_code = 400
    except IntegrityError as err:
        resText = 'unchecked db error'
        if 'UNIQUE' in err.args[0]:
            resText = 'employeeID already exists'
        res = make_response(resText)
        res.status_code = 400
    return res
        
@app.route("/shifts", methods=['POST'])
def create_shift():
    try:
        data = request.get_json()

        position = data['position']
        startDateTime = data['startDateTime']
        endDateTime = data['endDateTime']
        executionTime = data['executionTime']
        
        dbF.insert_shift(position, startDateTime, endDateTime, executionTime)

        res = make_response('Successfully created shift')
        res.status_code = 201
    except KeyError:
        res = make_response('Request requires position, startDateTime, endDateTime, executionTime (ISO time format)')
        res.status_code = 400
    return res

@app.route("/availability", methods=['POST'])
def create_availability():
    try:
        data = request.get_json()

        employeeID = data['employeeID']
        date = data['date']

        dbF.insert_availability(employeeID, date)

        res = make_response('Successfully created availability')
        res.status_code = 201
    except KeyError:
        res = make_response('Request requires employeeID, date yyyy-mm-dd')
        res.status_code = 400
    except IntegrityError as err:
        resText = 'unchecked db error'
        if 'UNIQUE' in err.args[0]:
            resText = 'duplicate entry'
        elif 'FOREIGN' in err.args[0]:
            resText = 'employeeID does not exist'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/bids", methods=['POST'])
def create_bid():
    try:
        data = request.get_json()

        employeeID = data['employeeID']
        shiftID = data['shiftID']

        dbF.insert_bid(employeeID, shiftID)

        res = make_response('Successfully created bid')
        res.status_code = 201
    except KeyError:
        res = make_response('Request requires employeeID, shiftID')
        res.status_code = 400
    except IntegrityError as err:
        resText = 'unchecked db error'
        if 'UNIQUE' in err.args[0]:
            resText = 'duplicate entry'
        elif 'FOREIGN' in err.args[0]:
            resText = 'employeeID or shiftID does not exist'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/employees/employeeID", methods=['PUT'])
def update_employee_employeeID():
    try:
        data = request.get_json()

        employeeID = data['employeeID']
        newID = data['newID']

        dbF.update_employee_employeeID(employeeID, newID)

        res = make_response('Successfully updated employeeID')
        res.status_code = 200
    except KeyError:
        res = make_response('Request requires employeeID, newID')
        res.status_code = 400
    except IntegrityError as err:
        resText = 'unchecked db error'
        if 'UNIQUE' in err.args[0]:
            resText = 'newID already exists, IDs must be unique'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/employees/phone", methods=['PUT'])
def update_employee_phone():
    try:
        data = request.get_json()

        employeeID = data['employeeID']
        phone = data['phone']

        dbF.update_employee_phone(employeeID, phone)

        res = make_response('Successfully updated phone')
        res.status_code = 200
    except KeyError:
        res = make_response('Request requires employeeID, phone')
        res.status_code = 400
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/employees/email", methods=['PUT'])
def update_employee_email():
    try:
        data = request.get_json()

        employeeID = data['employeeID']
        email = data['email']

        dbF.update_employee_email(employeeID, email)

        res = make_response('Successfully updated email')
        res.status_code = 200
    except KeyError:
        res = make_response('Request requires employeeID, email')
        res.status_code = 400
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/employees/notifications", methods=['PUT'])
def update_employee_notifications():
    try:
        data = request.get_json()

        employeeID = data['employeeID']
        notifications = data['notifications']

        dbF.update_employee_notifications(employeeID, notifications)

        res = make_response('Successfully updated notifications')
        res.status_code = 200
    except KeyError:
        res = make_response('Request requires employeeID, notifications')
        res.status_code = 400
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/shifts/status", methods=['PUT'])
def update_shift_status():
    try:
        data = request.get_json()

        shiftID = data['shiftID']
        status = data['status']

        dbF.update_shift_status(shiftID, status)

        res = make_response('Successfully updated shift status')
        res.status_code = 200
    except KeyError:
        res = make_response('Request requires shiftID, status')
        res.status_code = 400
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/shifts/assignee", methods=['PUT'])
def update_shift_assignee():
    try:
        data = request.get_json()

        shiftID = data['shiftID']
        assignee = data['assignee']

        dbF.update_shift_assignee(shiftID, assignee)

        res = make_response('Successfully updated shift assignee')
        res.status_code = 200
    except KeyError:
        res = make_response('Request requires shiftID, assignee')
        res.status_code = 400
    except IntegrityError as err:
        resText = 'unchecked db error'
        if 'FOREIGN' in err.args[0]:
            resText = 'employeeID does not exist'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/shifts/assignShift", methods=['PUT'])
def update_shift_assignShift():
    try:
        data = request.get_json()

        shiftID = data['shiftID']
        assignee = data['assignee']

        dbF.update_shift_assign_shift(shiftID, assignee)

        res = make_response('Successfully assigned shift')
        res.status_code = 200
    except KeyError:
        res = make_response('Request requires shiftID, assignee')
        res.status_code = 400
    except IntegrityError as err:
        resText = 'unchecked db error'
        if 'FOREIGN' in err.args[0]:
            resText = 'assignee employeeID does not exist'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/shifts/cancelShift", methods=['PUT'])
def update_shift_cancelShift():
    try:
        data = request.get_json()

        shiftID = data['shiftID']

        dbF.update_shift_cancel_shift(shiftID)

        res = make_response('Successfully cancelled shift')
        res.status_code = 200
    except KeyError:
        res = make_response('Request requires shiftID')
        res.status_code = 400
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/availability", methods=['DELETE'])
def delete_availability():
    try:
        data = request.get_json()

        employeeID = data['employeeID']
        date = data['date']

        dbF.delete_availability(employeeID, date)

        res = make_response('Successfully deleted availability')
        res.status_code = 200
    except KeyError:
        res = make_response('Request requires employeeID, date')
        res.status_code = 400
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/bids", methods=['DELETE'])
def delete_bid():
    try:
        data = request.get_json()

        employeeID = data['employeeID']
        shiftID = data['shiftID']

        dbF.delete_bid(employeeID, shiftID)

        res = make_response('Successfully deleted bid')
        res.status_code = 200
    except KeyError:
        res = make_response('Request requires employeeID, shiftID')
        res.status_code = 400
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/employees/id/<employeeID>", methods=['GET'])
def read_employee(employeeID):
    try:
        dbOutput = dbF.read_employee(employeeID)
        res = make_response(dbOutput)
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    except ItemNotFound:
        resText = f'Employee with ID "{employeeID}" not found'
        res = make_response(resText)
        res.status_code = 404
    return res

@app.route("/employees/id/<employeeID>/phone", methods=['GET'])
def read_employee_phone(employeeID):
    try:
        dbOutput = dbF.read_employee_phone(employeeID)
        res = make_response(dbOutput)
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    except ItemNotFound:
        resText = f'Employee with ID "{employeeID}" not found'
        res = make_response(resText)
        res.status_code = 404
    return res

@app.route("/employees/id/<employeeID>/email", methods=['GET'])
def read_employee_email(employeeID):
    try:
        dbOutput = dbF.read_employee_email(employeeID)
        res = make_response(dbOutput)
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    except ItemNotFound:
        resText = f'Employee with ID "{employeeID}" not found'
        res = make_response(resText)
        res.status_code = 404
    return res

@app.route("/employees/id/<employeeID>/notifications", methods=['GET'])
def read_employee_notifications(employeeID):
    try:
        dbOutput = dbF.read_employee_notifications(employeeID)
        res = make_response(dbOutput)
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    except ItemNotFound:
        resText = f'Employee with ID "{employeeID}" not found'
        res = make_response(resText)
        res.status_code = 404
    return res

@app.route("/shifts/id/<shiftID>", methods=['GET'])
def read_shift(shiftID):
    try:
        dbOutput = dbF.read_shift(shiftID)
        res = make_response(dbOutput)
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    except ItemNotFound:
        resText = f'Shift with ID "{shiftID}" not found'
        res = make_response(resText)
        res.status_code = 404
    return res

@app.route("/shifts/assignee/<assignee>", methods=['GET'])
def read_shifts_by_assignee(assignee):
    try:
        dbOutput = dbF.read_shifts_by_assignee(assignee)
        res = make_response({"shiftList": dbOutput})
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/shifts/unassigned", methods=['GET'])
def read_shifts_unassigned():
    try:
        dbOutput = dbF.read_shifts_unassigned()
        res = make_response({"shiftList": dbOutput})
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/shifts/pending", methods=['GET'])
def read_shifts_pending():
    try:
        dbOutput = dbF.read_shifts_pending()
        res = make_response({"shiftList": dbOutput})
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/shifts/pending/pastExecution", methods=['GET'])
def read_shifts_pending_past_execution():
    try:
        dbOutput = dbF.read_shifts_pending_past_execution()
        res = make_response({"shiftList": dbOutput})
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/shifts/assigned", methods=['GET'])
def read_shifts_assigned():
    try:
        dbOutput = dbF.read_shifts_assigned()
        res = make_response({"shiftList": dbOutput})
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/shifts/cancelled", methods=['GET'])
def read_shifts_cancelled():
    try:
        dbOutput = dbF.read_shifts_cancelled()
        res = make_response({"shiftList": dbOutput})
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/availability/employee/<employeeID>/<month>", methods=['GET'])
def read_availability_by_employee_and_month(employeeID, month):
    try:
        dbOutput = dbF.read_availability_by_employee_and_month(employeeID, month)
        res = make_response({"datesList": dbOutput})
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/availability/day/<day>", methods=['GET'])
def read_availability_by_day(day):
    try:
        dbOutput = dbF.read_availability_by_day(day)
        res = make_response({"employeeList": dbOutput})
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/bids/shift/<shiftID>", methods=['GET'])
def read_bids_employees_by_shift(shiftID):
    try:
        dbOutput = dbF.read_bids_employees_by_shift(shiftID)
        res = make_response({"employeeList": dbOutput})
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res

@app.route("/bids/employee/<employeeID>", methods=['GET'])
def read_bids_shifts_by_employee(employeeID):
    try:
        dbOutput = dbF.read_bids_shifts_by_employee(employeeID)
        res = make_response({"shiftList": dbOutput})
        res.status_code = 200
    except IntegrityError:
        resText = 'unchecked db error'
        res = make_response(resText)
        res.status_code = 400
    return res
