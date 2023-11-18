import 'package:flutter/material.dart';

import 'home.dart';

// void main() {
//   runApp(MyApp());
// }

void main() {
  runApp(
    MyApp(),

  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Cassia',
      theme: ThemeData(
        fontFamily: 'Montserrat',
        primaryColor: Colors.indigo//Color.fromRGBO(255, 63, 111, 1),
      ),
      home: Scaffold(
        body: NavigationBarPage(selectedIndex: 0,),
      ),
    );
  }
}
