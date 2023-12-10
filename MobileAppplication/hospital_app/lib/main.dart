import 'package:flutter/material.dart';
import 'package:logging/logging.dart';
import 'home.dart';


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
      home: Scaffold(
        body: NavigationBarPage(selectedIndex: 0,),
      ),
    );
  }
}
