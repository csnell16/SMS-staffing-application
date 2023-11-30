from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask import Flask, request, jsonify
import sched
import time
import datetime
app = Flask(__name__)
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)


request_id = 54168413  # Replace with actual request ID
phone_numbers2 = ["",""]  # RejectedPhoneNumbers
listOFavailableStaffNumbers=["",""]
scheduler = sched.scheduler(time.time, time.sleep)
shiftDataFromDBAndNumberOfWinner=[""]


def getPhoneNumbersOfAvailableStaffs():
    #need a method for each phoneNumberList above
    pass

@app.route('/getCancelShift', methods=['GET'])
def cancelShift():

    data = {
        'name': 'Example',
        'age': 30,
        'location': 'World'
    }
    return jsonify(data)

@app.route('/getOpenShiftRequests', methods=['GET'])
def getOpenShiftRequests():

    data = {
        'name': 'Example',
        'age': 30,
        'location': 'World'
    }
    return jsonify(data)

@app.route('/getScheduledShiftRequests', methods=['GET'])
def getScheduledShiftRequests():

    data = {
        'name': 'Example',
        'age': 30,
        'location': 'World'
    }
    return jsonify(data)




@app.route('/')
def hello():
    return "Shift Management System"

def send_sms(sender,messageSend):
    message = client.messages.create(
            body=messageSend, 
            from_='+15075735578',
            to=sender
    )


@app.route('/shiftCreation', methods=['POST'])
def shiftCreate():
    data = request.json

    # # Unpack the data directly from the request
    # position = data.get('position', 'Doctor')  # Provide default values
    # selected_date = data.get('selectedDate', '5/12/2023')
    # reply_deadline = data.get('replyDeadline', '5/13/2023 14:20')
    # from_time = data.get('fromTime', '07:00')
    # to_time = data.get('toTime', '19:00')

    # # Formatting the message using f-string for clarity
    # message_body = (f"You have received a Shift Position:\n"
    #                 f"To accept request reply ACCEPT {requestID}\n\n"
    #                 f"Shift Request ID: {requestID}\n"
    #                 f"Position: {position}\n"
    #                 f"Date: {selected_date}\n"
    #                 f"From Time: {from_time}\n"
    #                 f"To Time: {to_time}\n"
    #                 f"Reply By: {reply_deadline}")

    requestID=894816
    position ="Doctor" #data.get('position')
    selected_date ="5/12/2023" #data.get('selectedDate')
    reply_deadline ="5/13/2023 14:20"# data.get('replyDeadline')
    from_time = "07:00"#data.get('fromTime')
    to_time = "19:00"#data.get('toTime')
    message_body = (f"You have recieved a Shift Position:\nTo accept request reply ACCEPT {requestID}\n\nThe following are the Shift details:\n"f"Shift Request ID: {requestID}\n"
                        f"Position: {position}\n"
                        f"Date: {selected_date}\n"
                        f"From Time: {from_time}\n"
                        f"To Time: {to_time}\n"
                        f"Reply By: {reply_deadline}")
    
    for number in listOFavailableStaffNumbers:
        send_sms(number, message_body)
    print(message_body)








def schedule_shift_operations(execution_time, phone_numbers2,shiftDataFromDBAndNumberOfWinner):
    now = datetime.datetime.now()
    delay = (execution_time - now).total_seconds()

    scheduler.enter(delay, 1, submit_shift_request, argument=(shiftDataFromDBAndNumberOfWinner,))
    scheduler.enter(delay + 5, 1, handleRejectionMessage, argument=(phone_numbers2,))

    scheduler.run()







@app.route('/sms_webhook', methods=['POST'])
def sms_webhook():
    print("requestHere")

    print(request)
    message_body = request.form['Body']
    sender = request.form['From']

    # Example: Parsing a message that starts with "ACCEPT"
    if message_body.upper().startswith("ACCEPT"):
        return handle_accept_command(message_body, sender)
    # Add more conditions here for different types of messages
    else:
        return handle_default_response(sender)

    # return jsonify(status='success'), 200

def handle_accept_command(message, sender):
    # Logic for processing the ACCEPT command
    # Extract further details if necessary, e.g., "ACCEPT <ShiftID>"
    parts = message.split()
    if len(parts) >= 2:
        requestIDFromUser = parts[1]
        if(requestIDFromUser=="CHECK DB if its a valid RequestID and respond accodingly"):
            pass
        
        confirmationMessage(sender)



        execution_time = datetime.datetime(2023, 5, 12, 18, 0)  # Example time
        schedule_shift_operations(execution_time, phone_numbers2,shiftDataFromDBAndNumberOfWinner)

        # At execution time the follwing funtcions is executed
        # submit_shift_request(shiftDataFromDBAndNumberOfWinner)
        # time.sleep(5) # Sleep for 3 seconds
        # handleRejectionMessage(phone_numbers2)


    return jsonify(status='success'), 200
def handleRejectionMessage(phone_numbers2):
    for number in phone_numbers2:
        send_sms(number, "Unfortunetly the shift was assigned to another staff number. Thank you for applying, we appreciate it.")

    return jsonify(status='success'), 200

def handle_default_response(sender):
    send_sms(sender, "Unrecognized command. Please send a valid response:\nACCEPT <RequestID>")
    return jsonify(status='success'), 200

def submit_shift_request(shiftDataFromDBAndNumberOfWinner):
    # data = request.json

    position ="Doctor" #data.get('position')
    selected_date ="5/12/2023" #data.get('selectedDate')
    reply_deadline ="5/13/2023 14:20"# data.get('replyDeadline')
    from_time = "07:00"#data.get('fromTime')
    to_time = "19:00"#data.get('toTime')

    # Create the SMS message
    message_body = (f"Shift Request ID: {request_id} has been confirmed\n"
                    f"Position: {position}\n"
                    f"Date: {selected_date}\n"
                    f"From Time: {from_time}\n"
                    f"To Time: {to_time}\n")

    # Send the message to each phone number
    for number in shiftDataFromDBAndNumberOfWinner:
        send_sms(number,message_body)

    return jsonify({"message": "Shift request received and SMS sent"}), 200

def confirmationMessage(sender):
    send_sms(sender, "Thank you for applying for the shift. There are {5} other staff members who have applied as well.\nYou will be notified at {DATE-TIME} on the results.")
    return jsonify(status='success'), 200

if __name__ == "__main__":
    app.run(debug=True)
