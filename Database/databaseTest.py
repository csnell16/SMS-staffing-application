import sqlite3
import databaseFunctions as dbF

# this file is meant for manual testing and function test examples

# DATABASE_FILE = './database.db'

# connection = sqlite3.connect(DATABASE_FILE)
# cursor = connection.cursor()
# connection.close()

# ************ INSERT TESTS ************
# INSERT EMPLOYEES
# inserting should insert the first and third row. It should error the duplicate entry
# insert_employee('1', '123456789', 'mmmmhhggghh@mailinator.com', 0)
# insert_employee('1', '123456789', 'mmmmhhggghh@mailinator.com', 0)
# insert_employee('3', '123456789', 'mmkkkekekh@mailinator.com', 1)
# insert_employee('6', '123456789', 'mmmllllllleeeghh@mailinator.com')

# INSERT SHIFTS
# inserting shifts should give unique shift ids, status should be 0, assignee should be null
# insert_shift('doctor', '2023-11-09 08:00:00','2023-11-09 18:00:00', '2023-11-09 06:00:00')
# insert_shift('nurse', '2023-11-19 08:00:00', '2023-11-09 12:00:00', '2023-11-19 05:00:00')
# insert_shift('hr', '2023-12-10 08:00:00', '2023-11-09 09:00:00', '2023-12-10 05:00:00')

# INSERT AVAILABILITY
# ensure duplicate tuples are ignored on insert
# ensure employeeIDs are available in employees table and are not NULL

# insert_availability('1', '2023-11-09')
# insert_availability('1', '2023-11-09')
# insert_availability('1', '2023-11-27')
# insert_availability('3', '2023-12-10')
# insert_availability('2', '2023-11-09')
# insert_availability(None, '2023-11-09')

# insert_bid('1', '1')
# insert_bid('1', '3')
# insert_bid('1', '4')
# insert_bid('3', '3')
# insert_bid('99', '103')

# ************ UPDATE TESTS ************
# ensure value is changed for correct entry
# ensure primary keys are respected(no duplicates)

# first update should work, second should fail to primary key check
# update_employee_employeeID('1', '4')
# update_employee_employeeID('1', '4')
# update_employee_employeeID('81', '9')

# update_employee_phone('4', '4112223333')
# update_employee_phone('4', '3112223333')
# update_employee_phone('81', '99999')

# update_employee_email('4', 'bbbbggghhhgghhhggghh@mailinator.com')
# update_employee_email('3', 'bbbbggghhhjjhhggghh@mailinator.com')
# update_employee_email('81', 'bbbbmmmmmmmhhggghh@mailinator.com')

# update_employee_notifications('1', 1)
# update_employee_notifications('4', 0)
# update_employee_notifications('81', 99999)

# update_shift_status('1', 6)
# update_shift_status('81', 99999)

# assignee should have foreign key existing
# update_shift_assignee('4', 1)
# update_shift_assignee('5', 'mark')
# update_shift_assignee('81', 4)

# update_shift_assign_shift('4', 1)
# update_shift_assign_shift('3', 3, 0)


# update_shift_assign_shift('14', 'pp2')
# update_bids_winner('14', 'pp2')

# update_shift_cancel_shift('14')
# update_bids_cancelled_shift('14')

# ************ DELETE TESTS ************
# check availabilty that exists is deleted
# check availabilty that does not exist or does not match is unaffected
# delete_availability('1', '2023-11-09')
# delete_availability('7', '2023-11-09')
# delete_availability('7', '2023-11-27')

# delete_bid('1', '1')
# delete_bid('1', '3')
# delete_bid('99', '103')

# ************ READ TESTS ************

# print(read_employee('1'))
# print(read_employee('3'))
# print(read_employee('91'))

# print(read_employee_phone('1'))
# print(read_employee_phone('3'))
# print(read_employee_phone('91'))

# print(read_employee_email('1'))
# print(read_employee_email('3'))
# print(read_employee_email('91'))

# print(read_employee_email('1'))
# print(read_employee_email('3'))
# print(read_employee_email('91'))

# print(read_employee_notifications('1'))
# print(read_employee_notifications('3'))
# print(read_employee_notifications('91'))

# print(read_shift('1'))
# print(read_shift('3'))
# print(read_shift('-91'))

# print(read_shifts_by_assignee('1'))
# print(read_shifts_by_assignee(None))
# print(read_shifts_by_assignee('91'))

# print(read_shifts_pending())

# print(read_shifts_pending_past_execution())

# print(read_availability_by_employee_and_month('1', '2023-11'))
# print(read_availability_by_employee_and_month('1', '2023-12'))
# print(read_availability_by_employee_and_month('3', '2023-11'))
# print(read_availability_by_employee_and_month('3', '2023-12'))

# print(read_availability_by_day('2023-11-09'))
# print(read_availability_by_day('2023-11-27'))
# print(read_availability_by_day('2023-12-10'))
# print(read_availability_by_day('2024-01-22'))

# print(read_bids_employees_by_shift('1'))
# print(read_bids_employees_by_shift('3'))
# print(read_bids_employees_by_shift('91'))

# print(read_bids_shifts_by_employee('1'))
# print(read_bids_shifts_by_employee('3'))
# print(read_bids_shifts_by_employee('103'))

# insert_availability('1', '2023-11-09')
# insert_availability('1', '2023-11-27')
# insert_availability('3', '2023-11-09')
# print(read_availability_phone_by_day('2023-11-01'))
# print(read_availability_phone_by_day('2023-11-09'))
# print(read_availability_phone_by_day('2023-11-27'))

# insert_bid('1', '6')
# insert_bid('1', '5')
# insert_bid('3', '6')
# print(read_bids_employees_phone_by_shift('5'))
# print(read_bids_employees_phone_by_shift('6'))
# print(read_bids_employees_phone_by_shift('-3'))

# ************ OTHER TESTS **************
# print(read_distribution_by_shift_pending_bids('20'))
# print(read_distribution_by_availability_date('2023-12-27'))
# print(read_distribution_by_availability_date('2023-12-28'))
# print(read_distribution_by_availability_date('2023-12-29'))
# print(read_distribution_by_availability_date('2023-12-29 08:00:00'))
# update_distribution_assign_reinsert('pp99', DistributionStatus.MANUALLY_PUSHED_BACK.name)
# print(update_shift_auto_assign('20'))
# print(update_shift_auto_assign('25', True))

# ************ TEST DB SETUP ************

# insert_employee('4', '1234567893', 'mmmmhhggghh@mailinator.com', 0)
# insert_employee('1', '123456789', 'mmmmhhggghh@mailinator.com', 0)
# insert_employee('3', '123456789', 'mmkkkekekh@mailinator.com', 1)
# insert_employee('6', '123456789', 'mmmllllllleeeghh@mailinator.com')

# insert_shift('doctor', '2023-11-09 08:00:00','2023-11-09 18:00:00', '2023-11-09 06:00:00')
# insert_shift('nurse', '2023-11-19 08:00:00', '2023-11-09 12:00:00', '2023-11-19 05:00:00')
# insert_shift('hr', '2023-12-10 08:00:00', '2023-11-09 09:00:00', '2023-12-10 05:00:00')

# insert_availability('1', '2023-11-09')
# insert_availability('1', '2023-11-27')
# insert_availability('3', '2023-12-10')

# print(read_shifts_pending())
# print(read_shifts_pending_past_execution())
# print(read_availability_by_employee_and_month('1', '2023-11'))
# print(read_availability_by_employee_and_month('1', '2023-12'))
# print(read_availability_by_employee_and_month('3', '2023-11'))
# print(read_availability_by_employee_and_month('3', '2023-12'))

