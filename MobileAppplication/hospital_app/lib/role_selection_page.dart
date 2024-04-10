import 'package:flutter/material.dart';

class RoleSelectionPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.bottomCenter,
            end: Alignment.topCenter,
            colors: [
              Colors.purple.shade900,
              Colors.lightBlueAccent,
            ],
          ),
        ),
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: 30),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              SizedBox(
                height: 80,
              ),
              CircleAvatar(
                radius: 110,
                backgroundImage: AssetImage('assets/EntryScreenImage.jpeg'),
              ),
              SizedBox(
                height: 30,
              ),
              Text(
                'Select Your Role',
                style: TextStyle(
                  fontSize: 30,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
                textAlign: TextAlign.center,
              ),
              SizedBox(
                height: 60,
              ),
              ElevatedButton(
                style: ButtonStyle(
                  backgroundColor:
                      MaterialStateProperty.all(Colors.lightBlue[600]),
                  padding: MaterialStateProperty.all(
                    EdgeInsets.symmetric(vertical: 20),
                  ),
                  shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                    RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(90),
                      side: BorderSide(color: Colors.white, width: 3.0),
                    ),
                  ),
                ),
                onPressed: () {
                  // Navigate to the Admin login page
                  Navigator.pushNamed(context, '/adminLogin');
                },
                child: Text(
                  'Admin',
                  style: TextStyle(color: Colors.white, fontSize: 20),
                ),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                style: ButtonStyle(
                  backgroundColor:
                      MaterialStateProperty.all(Colors.lightBlue[600]),
                  padding: MaterialStateProperty.all(
                    EdgeInsets.symmetric(vertical: 20),
                  ),
                  shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                    RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(90),
                      side: BorderSide(color: Colors.white, width: 3.0),
                    ),
                  ),
                ),
                onPressed: () {
                  // Navigate to the Employee login page
                  Navigator.pushNamed(context, '/employeeLogin');
                },
                child: Text(
                  'Employee',
                  style: TextStyle(color: Colors.white, fontSize: 20),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}