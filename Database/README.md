# Preface
This file is to give an overview on how to run the API, major components, and how they work.

For more specifics details on individual parts, check the comments in the code or the code itself.

# Dependencies
## Useful Tools
ngrok was used as a reverse proxy during development (https://ngrok.com/)

Postman was used to test API endpoints (https://www.postman.com/)

DB Browser for SQLite is useful to read the database.db file (https://sqlitebrowser.org/)

## For the API (python)
It is recommended by flask to run a python virtual environment.
The only python packages that were necessary to install for me were flask, Twilio, and apscheduler.

Depending on your environment, you may need to install more(or less).

The full list of dependencies and their versions are shown below:

Python version: Python 3.12.1

Package            Version
------------------ ------------
aiohttp            3.9.1

aiohttp-retry      2.8.3

aiosignal          1.3.1

APScheduler        3.10.4

attrs              23.1.0

blinker            1.7.0

certifi            2023.11.17

charset-normalizer 3.3.2

click              8.1.7

colorama           0.4.6

Flask              3.0.0

frozenlist         1.4.1

idna               3.6

itsdangerous       2.1.2

Jinja2             3.1.2

MarkupSafe         2.1.3

multidict          6.0.4

pip                23.2.1

PyJWT              2.8.0

pytz               2023.3.post1

requests           2.31.0

six                1.16.0

twilio             8.11.0

tzdata             2023.3

tzlocal            5.2

urllib3            2.1.0

Werkzeug           3.0.1

yarl               1.9.4

Other versions of python or it's packages might work, but in case of cases like function depreciation the above are what has been proven to run.

# Running the API
to run the flask API use the command:
```
python <path to databaseAPI.py> 
```
or
```
flask --app <path to databaseAPI.py> run
```
and it will run on localhost:5000 by default

to have it 'hosted' you can use ngrok as a reverse proxy to allow calls from the internet (not just local host)
```
ngrok http 5000
```
ngrok will give you a URL in https://dashboard.ngrok.com/cloud-edge/endpoints which will allow calls over the internet when the API is accessed through this link

# Major Components
## Database
### Tables
There are 5 tables currently (2023-12-20):
- employees
- shifts
- availability
- bids
- distribution

#### employees table
Description:
- Stores information regarding users

Attributes:
- employeeID
	- Text; can be anything
	- Primary key; this attribute must be unique between entries
- phone
	- Text; to work with Twilio a properly formatted phone number should be used (see [Additional Notes](#additional-notes))
- email
	- Text; can be anything; currently unused and unchecked
- notifications
	- Integer; please follow the enumerator to set this value
	- if no value is set for notifications on creation it will default to ON

#### shifts table
Description:
- Stores information regarding shifts
- Shifts should be cancelled rather than deleted
- start and end times come with dates to allow easier overnight shift if wanted

Attributes:
- shiftID
	- Integer; auto-increments;
	- can be set manually through a query, but the API currently only allows for the auto-incremented IDs to be used
- position
	- Text; can be anything
	- describes the position of the shift eg. doctor, nurse, janitor, line cook etc
- startDateTime
	- Text; Should be in ISO format to function properly
	- 'yyyy-mm-dd HH:MM:SS'
	- start time of the shift
- endDateTime
	- Text; Should be in ISO format to function properly
	- 'yyyy-mm-dd HH:MM:SS'
	- end time of the shift
- executionTime
	- Text; Should be in ISO format to function properly
	- 'yyyy-mm-dd HH:MM:SS'
	- The date+time of when the shift will be auto-assigned and notified (see [Shift Auto-Scheduler](#shift-auto-scheduler))
- status
	- Text; please follow the enumerator to set the value
	- describes what point in the process the shift is
		- pending assignment, assigned, cancelled, etc.
- assignee
	- Text; Foreign key references employeeID in [employees table](#employees-table)
		- an employee in the employees table must have the same ID to link it
		- if the employeeID being referenced gets updated, this assignee should get auto-updated since it's set to cascade
	- If no assignee, value should be NULL

#### availability table
Description:
- Stores information regarding an employee's available days
- The Primary key for this is the combination of (employeeID, date) so duplicate entries of the exact same employeeID and date together should not exist

Attributes:
- employeeID
	- Text; Foreign key references employeeID in [employees table](#employees-table)
- date
	- Text; Should be in ISO format to function properly
	- 'yyyy-mm-dd'

#### bids table
Description:
- Stores information regarding an employee's bids
- The Primary key for this is the combination of (employeeID, shiftID) so duplicate entries of the exact same employeeID and shiftID together should not exist

Attributes:
- employeeID
	- Text; Foreign key references employeeID in [employees table](#employees-table)
- shiftID
	- Text; Foreign key references shiftID in [shifts table](#shifts-table)
- bidStatus
	- Text; please use the enumerator to set the value
	- describes the state of the bid with respect to the shift
		- shift cancelled, employee was assigned/rejected, pending assignment

#### distribution table
Description:
- Stores information for the distribution list with regards to auto-assignments
- When an employee is added to the [employees table](#employees-table), a trigger automatically puts it to the back of the distribution list
- Not designed to be edited by users except in the case of manually pushing employees to the back of the list
- Meant to be accessed programmatically by assignment and  [auto-assignment](#auto-assignment) functions
- employees should always have exactly 1 pending entry in the table 

Attributes:
- employeeID
	- Text; Foreign key references employeeID in [employees table](# employees table)
- distOrder
	- Integer; auto-increments
	- lower order number --> first to be auto-assigned
- distStatus
	- Text; please use the enumerator to set this value
	- describes the status of the distribution entry
	- if the entry was used to assign an employee, this value should be updated and a new pending entry should be added into the table to maintain exactly 1 pending entry in the table
	- can be read by humans to find out where the distribution table was consulted for assignment 
- shiftID
	- Text; can be anything but should reference a shiftID in the [shifts table](#shifts-table)
	- not a foreign key to loosen restrictions on assignment and reduce possible errors that can occur when auto-assigning
	- more for humans to read to find out when and how a shift was assigned with respect to the table along with the distStatus

### Enumerators
- Enumerators are added to provide more consistency to fields and columns of the database.
- It will be easier to use a text editor to autofill 'TableColumns.employeeID.name' rather than mistype a string literal or field like 'employeID'
- Do note that enumerator name and enumerator value are separate values to be sure to check which enumerator uses which
- Enumerators can be extended if more database statuses or attributes are required

## Database API
Implements simple features of a CRUD app to allow creation, reading, updating, and deleting of data in the database and provide access to the information in a controlled environment.

- functions referencing dates should be using the built in sql date/time functions like date() so that consistent date formats are stored and referenced
- Some database fields don't have a method to delete to maintain database integrity since some table use foreign keys.
	- For example, when assigning an employee to a shift, the assignee attribute in the shift table will use the foreign key employeeID from the employees table
	- This will ensure that when you assign an employeeID to a shift, that employee exists as a row in the employees table and will throw an error if no employee with that ID exists
	- Foreign keys are generally safe to update and will update in other tables since they are set to cascade
- Notably, instead of updating or deleting a shift, it is recommended to cancel it
	- This is because bids are reliant on shiftIDs in the shift table and removing one rather than cancelling it will cause information faults between tables
- Also, instead of deleting an employee it is recommended to update their fields

## Twilio/SMS functions
- Originally created on the SMS/mobile app side of development
	- For more details check the SMS Application Documentation
- Currently (2023-12-20) endpoints work when run through postman
	- More testing between these endpoints and the mobile app is required
- Refactored to allow smooth database access
	- mobile app currently uses different names and formats for information than the database so adaptors/format converters exist to bridge this gap
- Can send SMS updates:
	- on shift assignments
	- new shifts that are created
	- confirmation and acceptance of shifts
	- shift cancellations
- SMS updates respect notification settings from the database
	- if a user has notifications off, assignment updates should not be sent
- Integrated with the [Shift Auto-Scheduler](#shift-auto-scheduler) to send shift updates sequentially after assignments as to avoid race conditions

## Shift Auto-Scheduler
- On API startup the scheduler adds [auto-assignment](#auto-assignment) jobs for every shift with pending status
	- Each job has a runtime taken from the execution time of the given shift
- When the execution time is reached, it will:
	- auto-assign the associated shift
	- Then notify employees based on their notification settings, and the status of the shift/assignment
- Does NOT currently auto-assign pending jobs past execution time on startup nor if shift was added with execution time before current time
	- query to get pending shifts past execution exists, but nothing automated is currently (2023-12-20) implemented to clean up these unaccounted for shifts

## Auto Assignment
- FORCE_ASSIGNMENT should be set to True/False depending on if you want available employees to be assignable in the case that no employees have applied for the shift
- Notifications are always performed after auto-assignments by the scheduler
- Shift-assignment process is documented in the function update_shift_assign_shift() and outlines what happens when a shift is assigned to an employee:
	- given a shiftID, assignee, and optional assignment type:
		- update the assignee attribute for the shift with associated ID in the database
		- update the bids associated with the shiftID based on the status and who was assigned to the shift
		- update the distribution list to put the assignee on the back of the list and mark the distStatus based on the assignment type
- Auto-assignment decision logic is documented in the update_shift_auto_assign() function and is used to auto-select an employee and then use the shift-assignment process to assign them and update the relevant tables:
	- given a shift ID get the shift data
		- if it is already assigned, keep the assignee and exit
		- if it was cancelled, do nothing to the shift and exit
		- if it was marked unassignable by a previous auto-assign call, try assigning again
	- get the distribution list with respect to the employees that bid/applied to the shift
		- if there is at least one bidder/applicant, assign the shift to the bidder/applicant lowest in the distribution list
	- If there were no bids/applicants, check if force assignment is enabled
	- If force assignment is disabled, then mark the shift as 'unable to assign' and exit
	- if force assignment is enabled then:
		- get the distribution list with respect to any employees with availability on the day of the shift
		- if there is at least one person available on the day of the shift, assign the shift to the available person lowest on the distribution list
		- if there are no people available that day, mark the shift as 'unable to assign' and exit

# Additional Notes
- Running flask in debug mode can cause some database functions to be called twice
- Database API requires twilio account_sid, auth_token, and SEND_PHONE to run
- Twilio requires properly formatted phone numbers to send SMS properly
	- +AXXXYYYZZZZ
	- A is area code, XYZ are the 7 phone digits
- dates/datetimes should be in ISO format for the database
	- https://www.sqlite.org/lang_datefunc.html

# Next Steps (if any)
The app should be fully functional in the current state (2023-12-20) but some notable places to improve the app are the following:
- stronger input validation
- clean up protocols for pending shifts past execution
- more defined protocols for notification settings
- deployment
- better API responses/returns
- more consistent response bodies between mobile app and database API
- more documentation
- more testing on all parts
- better testing practices
- CI/CD