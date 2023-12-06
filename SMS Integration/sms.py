from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask import Flask, request, jsonify
import sched
import time
import datetime
import uuid

app = Flask(__name__)

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)


def getPhoneNumbersOfAvailableStaffs(list_type):
    # Needs to Updated with DB INFO
    if list_type == 'available':
        # Query for available staff phone numbers
        return ['+', '+']
    elif list_type == 'rejected':
        # Query for rejected staff phone numbers
        return ['+', '+']
    elif list_type == 'winner':
        # Query for winner staff phone numbers
        return ['+']
    else:
        return []



@app.route('/getCancelShift', methods=['POST'])
def cancelShift():
    #GET data(RequestID) back from APP and query DB to delete and handle all future messages to that RequestID appropriately
    # Needs Error Handling
    print("CANCELED SHIFT")
    return jsonify({'status': 'success', 'message': 'Shift request CANCELED successfully.'}), 200


@app.route('/getOpenShiftRequests', methods=['GET'])
def getOpenShiftRequests():
    #Data From DB

    shift_requests = [
        {
            'requestID': "48464684",

            'position': "Doctor",
            'date': "2023-12-01",  # ISO format date
            'fromTime': "09:00",
            'toTime': "17:00",
            'replyDeadline': "2023-11-25T17:30:00",  # ISO format datetime
            'currentBids': "5",

        },
        {
            'requestID': "48464684",

            'position': "Nurse",
            'date': "2023-12-02",
            'fromTime': "08:00",
            'toTime': "16:00",
            'replyDeadline': "2023-11-26T17:30:00",
                        'currentBids': "55",

        },
        {
            'requestID': "48464684",
            'position': "NeuroSurgeon",
            'date': "2023-12-08",
            'fromTime': "08:00",
            'toTime': "16:00",
            'replyDeadline': "2023-12-2T17:30:00",
                        'currentBids': "1",

        },
        {
            'requestID': "48464684",
            'position': "Physicist",
            'date': "2023-12-02",
            'fromTime': "08:00",
            'toTime': "16:00",
            'replyDeadline': "2023-11-26T17:30:00"
        },

    ]
    return jsonify(shift_requests)

@app.route('/getScheduledShiftRequests', methods=['GET'])
def getScheduledShiftRequests():
    #Data From DB

    shift_requests = [
        {
            'requestID': "48464684",
            'position': "Doctor2",
            'date': "2023-12-01",  # ISO format date
            'fromTime': "09:00",
            'toTime': "17:00",
            'replyDeadline': "2023-11-25T17:30:00",  # ISO format datetime
                                    'currentBids': "1",

        },
        {
            'requestID': "48464684",
            'position': "Nurse",
            'date': "2023-12-02",
            'fromTime': "08:00",
            'toTime': "16:00",
            'replyDeadline': "2023-11-26T17:30:00",
                                    'currentBids': "1",

        },
        {
            'requestID': "48464684",
            'position': "NeuroSurgeon",
            'date': "2023-12-08",
            'fromTime': "08:00",
            'toTime': "16:00",
            'replyDeadline': "2023-12-2T17:30:00",
                                    'currentBids': "1",

        },
        {
            'requestID': "48464684",
            'position': "Physicist",
            'date': "2023-12-02",
            'fromTime': "08:00",
            'toTime': "16:00",
            'replyDeadline': "2023-11-26T17:30:00"
        },

    ]
    return jsonify(shift_requests)




@app.route('/')
def hello():
    return "Shift Management System"

def send_sms(sender,messageSend):
    message = client.messages.create(
            body=messageSend, 
            from_='+15075735578',
            to=sender
    )
    print("SMS Details")
    print(message.sid)
    print(message.status)
    print(message.date_sent)



@app.route('/shiftCreation', methods=['POST'])
def shiftCreate():
    data = request.json

    # Extract the data with default values if not provided
    position = data.get('position', 'Default Position')
    selected_date = data.get('selectedDate', 'Default Date')
    reply_deadline = data.get('replyDeadline', 'Default Reply Deadline')
    from_time = data.get('fromTime', 'Default From Time')
    to_time = data.get('toTime', 'Default To Time')

    # Generate a unique request ID for the shift request
    requestID = generate_unique_request_id()  # Placeholder for the actual function to generate unique ID

    # Formatting the message
    message_body = (f"You have received a Shift Position:\n"
                    f"To accept request reply ACCEPT {requestID}\n\n"
                    f"Shift Request ID: {requestID}\n"
                    f"Position: {position}\n"
                    f"Date: {selected_date}\n"
                    f"From Time: {from_time}\n"
                    f"To Time: {to_time}\n"
                    f"Reply By: {reply_deadline}")

    #Send SMS to available staff
    for number in getPhoneNumbersOfAvailableStaffs("available"):
        send_sms(number, message_body)

    print(message_body)

    # Return a successful response
    return jsonify({'status': 'success', 'message': 'Shift request sent successfully.'}), 200
import uuid
import hashlib

def generate_unique_request_id():
    # Implement logic to generate a unique request ID
    unique_string = str(uuid.uuid4())
    hash_object = hashlib.sha256(unique_string.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig[:6]  # Taking the first 6 characters











@app.route('/sms_webhook', methods=['POST'])
def sms_webhook():
    print("requestHere")

    print(request)
    message_body = request.form['Body']
    sender = request.form['From']

    # Example: Parsing a message that starts with "ACCEPT"
    if message_body.upper().startswith("ACCEPT"):
        return acceptMessage(message_body, sender)
    # Add more conditions here for different types of messages
    else:
        return defaultResponse(sender)

    # return jsonify(status='success'), 200







def acceptMessage(message, sender):
    # Logic for processing the ACCEPT command
    # Extract further details if necessary, e.g., "ACCEPT <ShiftID>"
    parts = message.split()
    if len(parts) >= 2:
        requestIDFromUser = parts[1]
        if(requestIDFromUser=="CHECK DB if its a valid RequestID and respond accodingly"):
            pass
        
        confirmationMessage(sender)




        # At execution time the follwing funtcions is executed
        shiftWinnerMessage()
        time.sleep(5)
        rejectionMessage()


    return jsonify(status='success'), 200




def shiftWinnerMessage():
    #Needs to Updated with DB INFO

    # data = request.json

    position ="Doctor" #data.get('position')
    selected_date ="5/12/2023" #data.get('selectedDate')
    from_time = "07:00"#data.get('fromTime')
    to_time = "19:00"#data.get('toTime')
    request_id = 54168413  # Replace with actual request ID

    # Create the SMS message
    message_body = (f"Shift Request ID: {request_id} has been confirmed\n"
                    f"Position: {position}\n"
                    f"Date: {selected_date}\n"
                    f"From Time: {from_time}\n"
                    f"To Time: {to_time}\n")

    # Send the message to each phone number
    shiftWinnerNumber=getPhoneNumbersOfAvailableStaffs('winner')

    for number in shiftWinnerNumber:# There should be just 1 number
        send_sms(number,message_body)

    return jsonify({"message": "Shift request received and SMS sent"}), 200





def rejectionMessage():
    numbers=getPhoneNumbersOfAvailableStaffs('rejected')

    for number in numbers:
        send_sms(number, "Unfortunetly the shift was assigned to another staff number. Thank you for applying, we appreciate it.")

    return jsonify(status='success'), 200

def defaultResponse(sender):
    send_sms(sender, "Unrecognized command. Please send a valid response:\nACCEPT <RequestID>")
    return jsonify(status='success'), 200


def confirmationMessage(sender):
    #Needs to Updated with DB INFO
    send_sms(sender, "Thank you for applying for the shift. There are {5} other staff members who have applied as well.\nYou will be notified at {DATE-TIME} on the results.")
    return jsonify(status='success'), 200




if __name__ == "__main__":
    app.run(debug=True)
    