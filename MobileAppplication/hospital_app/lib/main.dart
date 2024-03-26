import 'package:flutter/material.dart';
import 'package:logging/logging.dart';
import 'home.dart';
import 'role_selection_page.dart';


void main() {
  _setupLogging();
  runApp(
    const MyApp(),

  );
}
void _setupLogging() {
  Logger.root.level = Level.ALL;
  Logger.root.onRecord.listen((record) {
    print('${record.level.name}: ${record.time}: ${record.message}');
  });
}
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        fontFamily: 'Montserrat',
        primaryColor: Colors.indigo
      ),
      home: RoleSelectionPage(),
      routes: {
        '/adminLogin': (context) => AdminLoginPage(),
        '/employeeLogin': (context)=> EmployeeLoginPage(),
      }
    );
  }
}

class AdminLoginPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Replace with your AdminLoginPage implementation
    return Scaffold(
      appBar: AppBar(
        title: Text('Admin Login'),
      ),
      body: Center(
        child: Text('Admin Login Content goes here'),
      ),
    );
  }
}

class EmployeeLoginPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Replace with your EmployeeLoginPage implementation
    return Scaffold(
      appBar: AppBar(
        title: Text('Employee Login'),
      ),
      body: Center(
        child: Text('Employe Login Content goes here'),
      ),
    );
  }
}