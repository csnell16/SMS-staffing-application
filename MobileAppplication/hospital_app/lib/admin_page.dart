import 'package:flutter/material.dart';
import 'package:hospital_app/add_admin.dart';
import 'package:hospital_app/add_employee.dart';


class AddSelectionPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.bottomCenter,
            end: Alignment.topCenter,
            colors:[
              Colors.purple.shade900,
              Colors.lightBlueAccent,
            ] 
          ),
        ),
      
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: 30, vertical: 80),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              
              Container(
                margin: EdgeInsets.only(bottom: 60),
                child: const Text(
                  'Select a user to add',
                  style: TextStyle(
                    fontSize: 30,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
              ElevatedButton(
                style: ButtonStyle(
                  backgroundColor: MaterialStateProperty.all(Colors.lightBlue[600]),
                  padding: MaterialStateProperty.all(
                    const EdgeInsets.symmetric(vertical: 20),
                  ),
                  shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                    RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(90), 
                      side: const BorderSide(color: Colors.white, width: 3.0),
                    ),
                  ),
                ),
                onPressed: () {
                  Navigator.push(context,MaterialPageRoute(builder: (context) => const AddAdminPage()),);
                },
                child: const Text(
                  'Add Admin',
                  style: TextStyle(color: Colors.white, fontSize: 20),
                ),
              ),

              const SizedBox(height: 50),

              ElevatedButton(
                style: ButtonStyle(
                  backgroundColor: MaterialStateProperty.all(Colors.lightBlue[600]),
                  padding: MaterialStateProperty.all(
                    const EdgeInsets.symmetric(vertical: 20),
                    ),
                  shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                    RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(90), 
                      side: const BorderSide(color: Colors.white, width: 3.0), 
                    ),
                  ),
                ),
                onPressed: () {
                  Navigator.push(context,MaterialPageRoute(builder: (context) => const AddEmployeePage()),);
                },
                child: const Text(
                  'Add Employee',
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
