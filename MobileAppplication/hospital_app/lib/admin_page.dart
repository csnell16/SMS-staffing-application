import 'package:flutter/material.dart';
import 'package:hospital_app/add_admin.dart';
import 'package:hospital_app/add_employee.dart';


class AdminPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
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
        child:Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 200),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              
              Container(
                margin: EdgeInsets.only(bottom: 80),
                child: const Text(
                  'Select a User To Add',
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
      ),
    );
  }
}
