
import 'package:curved_navigation_bar/curved_navigation_bar.dart';
import 'package:flutter/material.dart';
import 'package:hospital_app/CreateShiftRequest.dart';

import 'OpenShiftsPage.dart';
import 'AssignedShiftsPage.dart';



class NavigationBarPage extends StatefulWidget {
  int selectedIndex;
  NavigationBarPage({super.key, required this.selectedIndex});
  @override
  _NavigationBarPageState createState() => _NavigationBarPageState();
}

class _NavigationBarPageState extends State<NavigationBarPage> {
  final List<Widget> _children = [
    const CreateShiftRequestPage(),

    const OpenShiftsListPage(),
    const AssignedShiftRequestsListPage(),

  ];
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBody: true,
      body: _children[widget.selectedIndex],
      bottomNavigationBar: CurvedNavigationBar(
        color: const Color(0xFF630f0b),
        backgroundColor: Colors.transparent,
        buttonBackgroundColor: Colors.white,
        height: 50,
        index: widget.selectedIndex,
        onTap: (index) {
          setState(() {
            widget.selectedIndex = index;
          });
        },
        items: const <Widget>[
          Icon(
            Icons.account_circle,
            size: 26,
            color: Colors.black,
          ),
          Icon(
            Icons.add_circle_outline,
            size: 26,
            color: Colors.black,
          ),
          Icon(
            Icons.list,
            size: 26,
            color: Colors.black,
          ),
        ],
      ),
    );
  }
}
