
import 'package:curved_navigation_bar/curved_navigation_bar.dart';
import 'package:flutter/material.dart';
import 'package:hospital_app/tsets.dart';

import 'Cart.dart';
import 'createRequest.dart';
import 'openRequests.dart';



// ignore: must_be_immutable
class NavigationBarPage extends StatefulWidget {
  int selectedIndex;
  NavigationBarPage({required this.selectedIndex});
  @override
  _NavigationBarPageState createState() => _NavigationBarPageState();
}

class _NavigationBarPageState extends State<NavigationBarPage> {
  final List<Widget> _children = [
    CreateShiftRequestPage33(),

    ShiftRequestsListPage22(shiftRequests: [],),
    ShiftRequestsListPage223(shiftRequests: []),

  ];
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBody: true,
      body: _children[widget.selectedIndex],
      bottomNavigationBar: CurvedNavigationBar(
        color: Color(0xFF630f0b),
        backgroundColor: Colors.transparent,
        buttonBackgroundColor: Colors.white,
        height: 50,
        index: widget.selectedIndex,
        onTap: (index) {
          setState(() {
            widget.selectedIndex = index;
          });
        },
        items: <Widget>[
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
