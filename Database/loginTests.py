import bcrypt

# Employee Login Test(if database is empty)

# The password you want to hash
password = "password"

# Generate a salt and hash the password
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Print the hashed password to use in your SQL insert
print(hashed_password)

#run login Tests.py --> python3 or python loginTests.py run

# sqlite3 database.db
# INSERT INTO employees (employeeID, phone, email, notifications, password) 
# VALUES ('1', '1234567890', 'employee@example.com', 1, '$2b$12$PMgBPDc4sugALjyGZ8Pll.8Q5TTT4kT7gPh.YZ3g0HnwJSgOZM/zK');


#---------------------------------------------------------------------------------------

#login Testing
#for IOS simulator var url = Uri.parse('http://localhost:5000/api/login');
#for Android simulator var url = Uri.parse('http://10.0.2.2:5000/api/login');