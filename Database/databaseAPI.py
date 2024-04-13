import sqlite3
from flask import Flask, request, make_response,jsonify
from sqlite3 import IntegrityError
import databaseFunctions as dbF
import bcrypt
from flask import jsonify
from databaseFunctions import ItemNotFound, get_db_connection

app = Flask(__name__)

# employee login API
@app.route('/employee/login', methods=['POST'])
def employee_login():
    data = request.get_json()
    email = data['email']
    password = data['password'].encode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        stored_password = user['password'].encode('utf-8')

        if bcrypt.checkpw(password, stored_password):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    else:
        return jsonify({"message": "User not found"}), 404
    
# Admin Login API
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data['email']
    password = data['password'].encode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        stored_password = user['password']

        if bcrypt.checkpw(password, stored_password):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    else:
        return jsonify({"message": "User not found"}), 404


# Adding Admin API
@app.route('/register/admin', methods=['POST'])
def register_admin():
    data = request.get_json()
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    notifications = data.get('notifications', 1)

    if not email or not phone or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE email = ?", (email,))
    admin = cursor.fetchone()
    if admin:
        conn.close()
        return jsonify({'error': 'Admin with this email already exists'}), 409

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute('INSERT INTO admins (email, phone, password, notifications) VALUES (?, ?, ?, ?)',
                (email, phone, hashed_password, notifications))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Admin registered successfully'}), 201

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
        
        shift = dbF.insert_shift(position, startDateTime, endDateTime, executionTime)
        insertShiftIntoScheduler(shift)

        res = make_response(f'Successfully created shift with ID {shift[dbF.TableColumns.shiftID.name]}')
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


#################### TWILIO/SMS FUNCTIONS ####################

from twilio.twiml.messaging_response import MessagingResponse
import hashlib
from logging.handlers import RotatingFileHandler
import logging
from twilio.rest import Client
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

# twilio credentials
SEND_PHONE = ''
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

logging.basicConfig(level=logging.INFO,
                    filename='app.log',#The file to log into
                    filemode='a',  # Append Logs to existing log file, or use 'w' for a new file every time
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


#To ensure that your log files do not grow too large,
handler = RotatingFileHandler('app.log', maxBytes=1000)# Will rotate the log files, keeping the file size under 10,000 bytes and keep a max of 3 log files
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger('').addHandler(handler)

def getPhoneNumbersOfAvailableStaffs(date):
    logging.info("Acquiring available phone Numbers from DB")
    try:
        dataList = dbF.read_availability_phone_by_day(date) # date in 'yyyy-mm-dd' format
        availablePhonesNotificationsOn = [employee[dbF.TableColumns.phone.name] for employee in dataList
                                          if employee[dbF.TableColumns.notifications.name] == dbF.Notifications.ON.value]
        return availablePhonesNotificationsOn
    except:
        logging.info("Error acquiring available phone Numbers from DB")
        return []

def getPhoneNumbersOfAppliedStaff(requestID, list_filter):
    logging.info(f"Acquiring applied phone Numbers from DB with filter {list_filter}")
    try:
        dataList = dbF.read_bids_employees_phone_by_shift(requestID)
        if list_filter == 'all': # Query for all staff phone numbers for the requestID
            queriedPhones = [employee[dbF.TableColumns.phone.name] for employee in dataList
                             if employee[dbF.TableColumns.notifications.name] == dbF.Notifications.ON.value]
        elif list_filter == 'rejected': # Query for only rejected staff phone numbers
            queriedPhones = [employee[dbF.TableColumns.phone.name] for employee in dataList
                             if employee[dbF.TableColumns.notifications.name] == dbF.Notifications.ON.value
                             and employee[dbF.TableColumns.bidStatus.name] == dbF.BidStatus.REJECTED.name]
        elif list_filter == 'cancelled': # Query for numbers if shift was cancelled
            queriedPhones = [employee[dbF.TableColumns.phone.name] for employee in dataList
                             if employee[dbF.TableColumns.notifications.name] == dbF.Notifications.ON.value
                             and employee[dbF.TableColumns.bidStatus.name] == dbF.BidStatus.SHIFT_CANCELLED.name]
        else: # Query for only winner staff phone numbers
            queriedPhones = [employee[dbF.TableColumns.phone.name] for employee in dataList
                             if employee[dbF.TableColumns.notifications.name] == dbF.Notifications.ON.value
                             and employee[dbF.TableColumns.bidStatus.name] == dbF.BidStatus.ASSIGNED.name]
        return queriedPhones
    except:
        logging.info("Error acquiring applied phone Numbers from DB")
        return []

@app.route('/getCancelShift', methods=['POST'])
def cancelShift():
    data = request.json
    requestID = data.get('requestID')

    if not requestID:
        logging.error("No requestID provided in the cancel request")
        return jsonify({'status': 'failed', 'message': 'RequestID is required.'}), 400
    else:
        # Query DB to delete and handle all future messages to that RequestID appropriately
        try:
            dbF.update_shift_cancel_shift(requestID)
        except:
            logging.info(f"Shift {requestID} has encountered an error on CANCEL")
            return jsonify({'status': 'failed', 'message': 'Shift request CANCEL encountered an error.'}), 500
        logging.info(f"Shift {requestID} has been Successfully Canceled")
        return jsonify({'status': 'success', 'message': 'Shift request CANCELED successfully.'}), 200

def bidCounter(shiftID):
    try:
        return len(dbF.read_bids_employees_by_shift(shiftID))
    except:
        return 0

def formatShiftsForMobile(shift_list):
    # formats database output shift list for mobile app
    shift_requests = []
    for shift in shift_list:
        requestID = shift[dbF.TableColumns.shiftID.name]
        date = datetime.fromisoformat(shift[dbF.TableColumns.startDateTime.name]).strftime('%Y-%m-%d')
        start = datetime.fromisoformat(shift[dbF.TableColumns.startDateTime.name]).strftime('%H:%M')
        end = datetime.fromisoformat(shift[dbF.TableColumns.endDateTime.name]).strftime('%H:%M')
        reply = datetime.fromisoformat(shift[dbF.TableColumns.executionTime.name]).strftime('%Y-%m-%d %H:%M:%S') # ISO format datetime
        bidCount = bidCounter(requestID)
        newObj = {
            'requestID': requestID,
            'position': shift[dbF.TableColumns.position.name],
            'date': date,
            'fromTime': start,
            'toTime': end,
            'replyDeadline': reply,
            'assignedToName': shift[dbF.TableColumns.assignee.name],
            'currentBids': bidCount
        }
        shift_requests.append(newObj)
    return shift_requests

@app.route('/getOpenShiftRequests', methods=['GET'])
def getOpenShiftRequests():
    try:
        # get list of shifts from DB that are pending execution then formats for mobile
        shift_requests = formatShiftsForMobile(dbF.read_shifts_pending())
    except:
        shift_requests = []
        logging.info("Error in reading and formatting pending shifts")

    logging.info("Sending list of all Open Shift Requests to App")
    return jsonify(shift_requests)

@app.route('/getScheduledShiftRequests', methods=['GET'])
def getScheduledShiftRequests():
    try:
        # get list of shifts from DB that are assigned then formats for mobile
        shift_requests = formatShiftsForMobile(dbF.read_shifts_assigned())
    except:
        shift_requests = []
        logging.info("Error in reading and formatting scheduled shifts")

    logging.info("Sending list of all Scheduled Shift Requests to App")
    return jsonify(shift_requests)

@app.route('/')
def hello():
    return "Shift Management System"

def sendSMS(sender, messageSend):
    message = client.messages.create(
            body=messageSend,
            from_=SEND_PHONE,
            to=sender
    )
    logging.info(f"'SMS Details':{message.sid},'Status:'{message.status},'Date Sent:'{message.date_sent}")

@app.route('/shiftCreation', methods=['POST'])
def shiftCreate():
    data = request.json
    # Extract the data with default values if not provided
    try:
        position = data.get('position', 'Default Position')
        selected_date = datetime.fromisoformat(data.get('selectedDate', '2024-01-01')).strftime("%Y-%m-%d")
        reply_deadline = datetime.fromisoformat(f"{selected_date} {data.get('replyDeadline', '08:00')}").strftime('%H:%M')
        from_time = datetime.fromisoformat(f"{selected_date} {data.get('fromTime', '09:00')}").strftime('%H:%M')
        to_time = datetime.fromisoformat(f"{selected_date} {data.get('toTime', '17:00')}").strftime('%H:%M')
    except:
        logging.info("Shift extraction failure: improper date/time format")
        return jsonify({'status': 'failure', 'message': 'selectedDate must be in yyyy-mm-dd format, times(replyDeadline, fromTime, toTime) must be in HH:MM format'}), 500

    # Store the shift in the database
    try:
        # fix iso format
        executionTime = f'{selected_date} {reply_deadline}:00'
        startDateTime = f'{selected_date} {from_time}:00'
        endDateTime = f'{selected_date} {to_time}:00'

        insertedObj = dbF.insert_shift(position, startDateTime, endDateTime, executionTime)
        requestID = insertedObj['shiftID']
    except:
        logging.info("Shift insertion error")
        return jsonify({'status': 'failure', 'message': 'Shift request insertion error'}), 500

    messageBody = (f"You have received a Shift Position:\n"
                    f"To accept request respond with:\nACCEPT {requestID}\n\n"
                    f"Shift Request ID: {requestID}\n"
                    f"Position: {position}\n"
                    f"Date: {selected_date}\n"
                    f"From Time: {from_time}\n"
                    f"To Time: {to_time}\n"
                    f"Respond By: {reply_deadline}")

    for number in getPhoneNumbersOfAvailableStaffs(selected_date):
        sendSMS(number, messageBody)
    logging.info("Shift has been Successfully created")

    return jsonify({'status': 'success', 'message': 'Shift request sent successfully.'}), 200

@app.route('/sms_webhook', methods=['POST'])
def sms_webhook():
    logging.info("Accepting SMS message from user")

    messageBody = request.form['Body']
    sender = request.form['From']

    if messageBody.upper().startswith("ACCEPT"):# Checking if the message is according to format
        return acceptMessage(messageBody, sender)
    else:
        return defaultResponse(sender)

def acceptMessage(message, sender):
    # parse message data and ensure correct format
    parts = message.split()
    if len(parts) >= 2:
        requestIDFromUser = parts[1]
    else:
        logging.info("Informing user they sent an Unrecognized command, not in the specified format")
        return defaultResponse(sender)

    # get shift data from database
    try:
        shift = dbF.read_shift(requestIDFromUser)
    except ItemNotFound:
        logging.info("Request ID given is not valid, Informed user to send a valid response")
        return sendSMS(sender, "Request ID given is not valid. Please send a valid response:\nACCEPT <RequestID>") # When the give RequestID is not found in DB
    except:
        logging.info("Unchecked error in acceptMessage")
        return sendSMS(sender, "Backend error, please try again later")

    # check if shift is cancelled and respond accordingly
    if(shift[dbF.TableColumns.status.name] == dbF.ShiftStatus.CANCELLED.name):
        logging.info("Informing user that RequestID shift has been canceled")
        return sendSMS(sender, "The Requested Shift has been canceled. Thank you for applying.")

    # since shift is not cancelled, put a bid for the employee on the shift
    # if there are multiple employees with the same phone, add them all to the shift
    try:
        employeeIDs = dbF.read_employees_by_phone(sender)
        for employeeID in employeeIDs:
            dbF.insert_bid(employeeID, requestIDFromUser)
    except Exception as err:
        if 'UNIQUE' in err.args[0]:
            logging.info("Employee already applied")
            return sendSMS(sender, f"You have already applied for shift {requestIDFromUser} at {shift[dbF.TableColumns.startDateTime.name]}")
        elif 'FOREIGN' in err.args[0]:
            # this should not occur at this point since requestIDs are validated and employeeIDs are from DB
            logging.info("Verification error creating bid from phone")
            return sendSMS(sender, f"Backend error, please try again later")
        else:
            logging.info("Unchecked error creating bid from phone")
            return sendSMS(sender, f"Backend error, please try again later")

    # bids are created
    logging.info("Confirming to user that they have applied to shift")
    # bid count
    currentBids = bidCounter(requestIDFromUser)
    notificationTime = shift[dbF.TableColumns.executionTime.name]
    confirmationMessage(sender, currentBids, notificationTime)
    return jsonify(status='success'), 200

def shiftWinnerMessage(requestID, shiftWinnerNumber):
    logging.info("Sending messages to the person who recieved the shift")
    try:
        shift = dbF.read_shift(requestID)
        position = shift[dbF.TableColumns.position.name]
        selected_date = datetime.fromisoformat(shift[dbF.TableColumns.startDateTime.name]).strftime("%Y-%m-%d")
        from_time = datetime.fromisoformat(shift[dbF.TableColumns.startDateTime.name]).strftime("%H:%M")
        to_time = datetime.fromisoformat(shift[dbF.TableColumns.endDateTime.name]).strftime("%H:%M")
    except ItemNotFound:
        logging.info(f"Shift with ID {requestID} not found")
        return
    except:
        logging.info(f"Unchecked error sending shift winner message")
        return

    # Create the SMS message
    messageBody = (f"Shift Request ID: {requestID} has been confirmed\n"
                    f"Position: {position}\n"
                    f"Date: {selected_date}\n"
                    f"From Time: {from_time}\n"
                    f"To Time: {to_time}\n")

    # Send the message to each phone number
    for number in shiftWinnerNumber: # There should be just 1 number
        sendSMS(number, messageBody)
    logging.info("200, Success in Sending messages to the person who recieved the shift")

def rejectionMessage(requestID, numbers):
    logging.info("Sending messages to rejected numbers for the shift")
    for number in numbers:
        sendSMS(number, f"Unfortunately shift {requestID} was assigned to another staff number. Thank you for applying, we appreciate it.")
    logging.info(f"200, Success in Sending messages to {len(numbers)} rejected numbers for shift {requestID}")

def cancelMessage(requestID, numbers):
    logging.info("Sending cancellation messages to applied numbers if request was cancelled")
    for number in numbers:
        sendSMS(number, f"Shift {requestID} has been cancelled. Thank you for applying, we appreciate it.")
    logging.info(f"200, Success in sending cancellation messagess to {len(numbers)} numbers for shift {requestID}")

def defaultResponse(sender):
    logging.info("Sending SMS message back to user, concerning Unrecognized command")

    sendSMS(sender, "Unrecognized command. Please send a valid response:\nACCEPT <RequestID>")
    return jsonify(status='success'), 200

def confirmationMessage(sender, currentBids, dateTime):
    logging.info("Sending corfirmation SMS message back to user")

    sendSMS(sender, "Thank you for applying for the shift. There are " + str(currentBids) + " other staff members who have applied as well.\nYou will be notified at " + str(dateTime) + " on the results.")
    return jsonify(status='success'), 200

#################### ASSIGNMENT/NOTIFICATION SCHEDULER ####################

from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler(daemon=True)

# set true to allows employees available on shift day to be selected if nobody accepted the shift
FORCE_ASSIGNMENT = True

def autoAssignAndNotify(shiftID):
    # Automatic shift assignment that triggers phone notifications to the applicants
    # ASSIGN MUST BE PERFORMED BEFORE SENDING TO AVOID RACE CONDITIONS
    try:
        logging.info(f"Auto-assigning shift with ID {shiftID}")
        employee = dbF.update_shift_auto_assign(shiftID, FORCE_ASSIGNMENT)
    except:
        logging.info(f"Error auto-assigning with shiftID {shiftID}")
        return
    # notify staff that applied
    try:
        logging.info(f"Sending Messages for shift with ID {shiftID}")
        rejectionMessage(shiftID, getPhoneNumbersOfAppliedStaff(shiftID, 'rejected'))
        cancelMessage(shiftID, getPhoneNumbersOfAppliedStaff(shiftID, 'cancelled'))

        # auto assign can assign a winner that has not applied
        winnerPhones = getPhoneNumbersOfAppliedStaff(shiftID, 'winner')
        if len(winnerPhones) == 0 and employee is not None:
            # get phone directly from employeeID if they did not apply and were force assigned
            if employee[dbF.TableColumns.notifications.name] == dbF.Notifications.OFF.value:
                winnerPhones = []
            else:
                winnerPhones = [employee[dbF.TableColumns.phone.name]]
        shiftWinnerMessage(shiftID, winnerPhones)
    except:
        logging.info(f"Error sending messages for shift with ID {shiftID}")
        return
    logging.info(f"Successfully auto-assigned and notified for shift with ID {shiftID}")

def insertShiftIntoScheduler(shiftObj):
    # inserts shift into the scheduler; shiftObj requires executionTime and shiftID
    executionTimeString = shiftObj.get(dbF.TableColumns.executionTime.name)
    shiftID = shiftObj.get(dbF.TableColumns.shiftID.name)
    try:
        if executionTimeString is None or shiftID is None:
            raise Exception
        executionTime = datetime.fromisoformat(executionTimeString)
        scheduler.add_job(autoAssignAndNotify, 'date', run_date=executionTime, args=[shiftID])
        logging.info(f"Scheduled shift with shiftID: {shiftID}, executionTime: {executionTimeString}")
    except:
        logging.info(f"Failed to schedule shift with shiftID: {shiftID}, executionTime: {executionTimeString}")

def initializeScheduler():
    # start scheduler and put intial pending jobs into the scheduler
    if not scheduler.running:
        scheduler.start()
        try:
            shifts = dbF.read_shifts_pending()
            for shift in shifts:
                insertShiftIntoScheduler(shift)
        except:
            logging.info("Error initializing assignment executor")

# run initializer
initializeScheduler()

if __name__ == "__main__":
    app.run(debug=False)