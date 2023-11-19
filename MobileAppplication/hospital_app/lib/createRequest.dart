import 'package:flutter/material.dart';

class ShiftRequest {
  final String position;
  final DateTime date;
  final TimeOfDay fromTime;
  final TimeOfDay toTime;
  final DateTime replyDeadline;

  ShiftRequest({
    required this.position,
    required this.date,
    required this.fromTime,
    required this.toTime,
    required this.replyDeadline,
  });
}
class ShiftRequestsListPage22 extends StatefulWidget {
  final List<ShiftRequest> shiftRequests;

  ShiftRequestsListPage22({Key? key, required this.shiftRequests}) : super(key: key);

  @override
  _ShiftRequestsListPageState createState() => _ShiftRequestsListPageState();
}

class _ShiftRequestsListPageState extends State<ShiftRequestsListPage22> {
  ShiftRequest? _selectedRequest; // State variable to track the selected request

  List<ShiftRequest> _shiftRequests=[
    ShiftRequest(
      position: "Cashier",
      date: DateTime(2023, 12, 1),
      fromTime: TimeOfDay(hour: 9, minute: 0),
      toTime: TimeOfDay(hour: 17, minute: 0),
      replyDeadline: DateTime(2023, 11, 25),
    ),
    ShiftRequest(
      position: "Barista",
      date: DateTime(2023, 12, 2),
      fromTime: TimeOfDay(hour: 8, minute: 0),
      toTime: TimeOfDay(hour: 16, minute: 0),
      replyDeadline: DateTime(2023, 11, 26),
    ),
    ShiftRequest(
      position: "Barista",
      date: DateTime(2023, 12, 2),
      fromTime: TimeOfDay(hour: 8, minute: 0),
      toTime: TimeOfDay(hour: 16, minute: 0),
      replyDeadline: DateTime(2023, 11, 26),
    ),      ShiftRequest(
      position: "Barista",
      date: DateTime(2023, 12, 2),
      fromTime: TimeOfDay(hour: 8, minute: 0),
      toTime: TimeOfDay(hour: 16, minute: 0),
      replyDeadline: DateTime(2023, 11, 26),
    ),      ShiftRequest(
      position: "Barista",
      date: DateTime(2023, 12, 2),
      fromTime: TimeOfDay(hour: 8, minute: 0),
      toTime: TimeOfDay(hour: 16, minute: 0),
      replyDeadline: DateTime(2023, 11, 26),
    ),      ShiftRequest(
      position: "Barista",
      date: DateTime(2023, 12, 2),
      fromTime: TimeOfDay(hour: 8, minute: 0),
      toTime: TimeOfDay(hour: 16, minute: 0),
      replyDeadline: DateTime(2023, 11, 26),
    ),
    // Add more objects as needed
  ];

  @override
  void initState() {
    super.initState();
    // _shiftRequests = widget.shiftRequests;
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[850], // Dark background like CreateShiftRequestPage33
      appBar: AppBar(
        title: Text(
          'Open Shift Request',
          textAlign: TextAlign.center,
          style: TextStyle(fontSize:22,color: Colors.white,fontWeight: FontWeight.bold,fontFamily:'Proxima Nova'),

        ),
        backgroundColor: Colors.deepPurple, // Updated color
        elevation: 4, // Shadow under the AppBar
        // actions: <Widget>[
        //   IconButton(
        //     icon: Icon(Icons.settings), // Example icon
        //     onPressed: () {
        //       // Action for settings or other functionality
        //     },
        //   ),
        // ],
        flexibleSpace: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              tileMode: TileMode.repeated,
              stops: [0.35, 0.90],

              colors: [Colors.purple, Colors.deepPurple], // Gradient colors

            ),
          ),
        ),
      ),
      body: ListView.builder(
        itemCount: _shiftRequests.length,
        itemBuilder: (context, index) {
          return _buildShiftRequestItem(context, _shiftRequests[index]);
        },
      ),
    );
  }

  Widget _buildShiftRequestItem(BuildContext context, ShiftRequest request) {
    bool isSelected = _selectedRequest == request;

    return GestureDetector(
      onLongPressDown: (_) => setState(() => _selectedRequest = request),
      onLongPressUp: () => setState(() => _selectedRequest = null),
      onLongPress: () => _showCancelConfirmation(context, request),
      child: Card(
        // color: isSelected ? Colors.red : Colors.white, // Change color when selected
        margin: EdgeInsets.symmetric(horizontal: 10, vertical: 15),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(15),
        ),
        shadowColor: Colors.grey.withOpacity(0.2),
        elevation: 5,
        child: InkWell(
          splashColor: Colors.red,
          onTap: () {}, // You can add functionality here if needed
          child: Column(
            children: [
              ListTile(
                contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                title: Text(
                  request.position,
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 20,
                    fontFamily: 'Proxima Nova',
                    color: Colors.black,
                  ),
                ),
                subtitle: Text(
                  'Date: ${_formatDate(request.date)}\nTime: ${_formatTime(request.fromTime)} - ${_formatTime(request.toTime)}',
                  style: _infoTextStyle(),
                ),
              ),
              Divider(thickness: 1, indent: 20, endIndent: 20, color: Colors.black),
              Padding(
                padding: EdgeInsets.fromLTRB(20, 5, 20, 10),
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    'Reply by: ${_formatDate(request.replyDeadline)}',
                    style: _infoTextStyle(),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  TextStyle _infoTextStyle() {
    return TextStyle(
      fontSize: 16,
      fontWeight: FontWeight.bold,
      color: Colors.black,
      fontFamily: 'Proxima Nova',
    );
  }

  String _formatDate(DateTime date) {
    return '${date.day.toString().padLeft(2, '0')}/${date.month.toString().padLeft(2, '0')}/${date.year}';
  }

  String _formatTime(TimeOfDay time) {
    final hour = time.hour.toString().padLeft(2, '0');
    final minute = time.minute.toString().padLeft(2, '0');
    return '$hour:$minute';
  }





  void _showCancelConfirmation(BuildContext context, ShiftRequest request) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Cancel Request'),
        content: Text('Are you sure you want to cancel this shift request for ${request.position}?'),
        actions: <Widget>[
          TextButton(
            onPressed: () {
              setState(() {
                _shiftRequests.remove(request);
              });
              Navigator.of(context).pop(); // Close the dialog
            },
            child: Text('Yes', style: TextStyle(color: Colors.red)),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(context).pop(); // Close the dialog without removing
            },
            child: Text('No'),
          ),
        ],
      ),
    );
  }
}
