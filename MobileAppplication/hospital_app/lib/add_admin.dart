import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'admin_login_page.dart';

class AddAdminPage extends StatefulWidget {
  const AddAdminPage({Key? key}) : super(key: key);

@override
  _AddAdminPageState createState() => _AddAdminPageState();
}

class _AddAdminPageState extends State<AddAdminPage> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _confirmPasswordController = TextEditingController();
  bool _receiveNotifications = false;
  bool _isLoading = false;

  void _addAdmin() async{
  String email = _emailController.text.trim();
  String phone = _phoneController.text.trim();
  String password = _passwordController.text.trim();
  String confirmPassword = _confirmPasswordController.text.trim();

  if (email.isEmpty || phone.isEmpty || password.isEmpty || confirmPassword.isEmpty) {
    _showDialog('Error', 'Please fill in all fields.');
    return;
  }

  if (!RegExp(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b').hasMatch(email)) {
    _showDialog('Error', 'Please enter a valid email address.');
    return;
  }

  if (!RegExp(r'^\d+$').hasMatch(phone)) {
    _showDialog('Error', 'Please enter a valid phone number.');
    return;
  }

  if (password != confirmPassword) {
    _showDialog('Error', 'Passwords do not match.');
    return;
  }

  var response = await http.post(
      Uri.parse('http://localhost:5000/register/admin'),
      headers: <String, String>{
        'Content-Type': 'application/json',
      },
      body: jsonEncode(<String, dynamic>{
        'email': email,
        'phone': phone,
        'password': password,
        'notifications': _receiveNotifications ? 1 : 0,
      }),
    );
    setState(() {
      _isLoading = true;
    });

    var rspns = await http.post(
      Uri.parse('http://localhost:5000/register/admin'),
      headers: <String, String>{
        'Content-Type': 'application/json',
      },
      body: jsonEncode(<String, dynamic>{
        'email': email,
        'phone': phone,
        'password': password,
        'notifications': _receiveNotifications ? 1 : 0,
      }),
    );

    setState(() {
      _isLoading = false;
    });

    if (response.statusCode == 201) {
      _showDialog('Success', 'Admin added successfully.');
      Navigator.of(context).pushReplacement(MaterialPageRoute(builder: (_) => const AdminLoginPage()));
    } else {
      Map<String, dynamic> result = jsonDecode(response.body);
      _showDialog('Failed', result['error'] ?? 'Unknown error occurred.');
    }

}

   void _showDialog(String title, String content) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(title),
        content: Text(content),
        actions: <Widget>[
          TextButton(
            child: const Text('OK'),
            onPressed: () {
              Navigator.of(context).pop();
            },
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Add Admin"),),
      body: Container(
        padding: const EdgeInsets.all(16),
        constraints: const BoxConstraints.expand(),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.bottomCenter,
            end: Alignment.topCenter,
            colors: [Colors.purple.shade900, Colors.lightBlueAccent],
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF120543),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  TextFormField(
                    controller: _emailController,
                    decoration: const InputDecoration(
                      hintText: 'Email',
                      hintStyle: TextStyle(color: Colors.white70, fontSize: 20),
                      enabledBorder: UnderlineInputBorder(
                        borderSide: BorderSide(color: Colors.white),
                      ),
                    ),
                    style: const TextStyle(color: Colors.white),
                  ),
                  TextFormField(
                    controller: _phoneController,
                    decoration: const InputDecoration(
                      hintText: 'Phone Number',
                      hintStyle: TextStyle(color: Colors.white70, fontSize: 20),
                      enabledBorder: UnderlineInputBorder(
                        borderSide: BorderSide(color: Colors.white),
                      ),
                    ),
                    style: const TextStyle(color: Colors.white),
                  ),
                  // const SizedBox(height: 20),
                  TextFormField(
                    controller: _passwordController,
                    obscureText: true,
                    decoration: const InputDecoration(
                      hintText: 'Password',
                      hintStyle: TextStyle(color: Colors.white70, fontSize: 20),
                      enabledBorder: UnderlineInputBorder(
                        borderSide: BorderSide(color: Colors.white),
                      ),
                    ),
                    style: const TextStyle(color: Colors.white),
                  ),
                  TextFormField(
                    controller: _confirmPasswordController,
                    obscureText: true,
                    decoration: const InputDecoration(
                      hintText: 'Confirm Password',
                      hintStyle: TextStyle(color: Colors.white70, fontSize: 20),
                      enabledBorder: UnderlineInputBorder(
                        borderSide: BorderSide(color: Colors.white),
                      ),
                    ),
                    style: const TextStyle(color: Colors.white),
                  ),
                 
                  CheckboxListTile(
                    title: const Text(
                      'Recieve Notifications',
                      style: TextStyle(color: Colors.white70),
                    ),
                    value: _receiveNotifications, // Initial value
                    onChanged: (bool? value) {
                      setState(() {
                        _receiveNotifications = value ?? false;
                      });
                    },
                    controlAffinity: ListTileControlAffinity.leading,
                    activeColor: Colors.white,
                    checkColor: Colors.lightBlueAccent,
                  ),
                  const SizedBox(height: 24),
                  ElevatedButton(
                      onPressed: _isLoading ? null : _addAdmin,
                      style: ElevatedButton.styleFrom(
                        foregroundColor: const Color(0xFF120543),
                        backgroundColor: const Color.fromARGB(255, 228, 160, 82),
                      ),
                      child: _isLoading 
                        ? const CircularProgressIndicator(color: Colors.white) 
                        : const Text(
                            'Add',  // Button text
                            style: TextStyle(fontSize: 16),  // Text size
                        ),
                    ),
                  ],
                ),
              ),
            ],
          ),
      )
    );
  }
}
