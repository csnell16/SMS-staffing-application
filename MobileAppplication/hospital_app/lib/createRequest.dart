import 'dart:convert';
import 'package:http/http.dart' as http;

import 'package:flutter/material.dart';


class ShiftRequestsListPage22 extends StatefulWidget {
  final List<ShiftRequest> shiftRequests;

  ShiftRequestsListPage22({Key? key, required this.shiftRequests}) : super(key: key);

  @override
  _ShiftRequestsListPageState createState() => _ShiftRequestsListPageState();
}

class _ShiftRequestsListPageState extends State<ShiftRequestsListPage22> {
  ShiftRequest? _selectedRequest; // State variable to track the selected request
  String API_ENDPOINT="https://5785-50-100-225-56.ngrok-free.app";

  // List<ShiftRequest> _shiftRequests=[
  //   ShiftRequest(
  //     position: "Cashier",
  //     date: DateTime(2023, 12, 1),
  //     fromTime: TimeOfDay(hour: 9, minute: 0),
  //     toTime: TimeOfDay(hour: 17, minute: 0),
  //     replyDeadline: DateTime(2023, 11, 25, 17, 30), // Deadline with specific time
  //   ),
  //   ShiftRequest(
  //     position: "Nurse",
  //     date: DateTime(2023, 12, 2),
  //     fromTime: TimeOfDay(hour: 8, minute: 0),
  //     toTime: TimeOfDay(hour: 16, minute: 0),
  //     replyDeadline: DateTime(2023, 11, 26, 17, 30), // Deadline with specific time
  //   ),
  //   ShiftRequest(
  //     position: "Surgeon",
  //     date: DateTime(2023, 12, 2),
  //     fromTime: TimeOfDay(hour: 8, minute: 0),
  //     toTime: TimeOfDay(hour: 16, minute: 0),
  //     replyDeadline: DateTime(2023, 11, 26, 17, 30), // Deadline with specific time
  //   ),      ShiftRequest(
  //     position: "Reception",
  //     date: DateTime(2023, 12, 2),
  //     fromTime: TimeOfDay(hour: 8, minute: 0),
  //     toTime: TimeOfDay(hour: 16, minute: 0),
  //     replyDeadline: DateTime(2023, 11, 26, 17, 30), // Deadline with specific time
  //   ),      ShiftRequest(
  //     position: "Doctor",
  //     date: DateTime(2023, 12, 2),
  //     fromTime: TimeOfDay(hour: 8, minute: 0),
  //     toTime: TimeOfDay(hour: 16, minute: 0),
  //     replyDeadline: DateTime(2023, 11, 26),
  //   ),      ShiftRequest(
  //     position: "Doctor",
  //     date: DateTime(2023, 12, 2),
  //     fromTime: TimeOfDay(hour: 8, minute: 0),
  //     toTime: TimeOfDay(hour: 16, minute: 0),
  //     replyDeadline: DateTime(2023, 11, 26),
  //   ),
  //   // Add more objects as needed
  // ];
  List<ShiftRequest> _shiftRequests = [];

  @override
  void initState() {
    super.initState();
    _fetchShiftRequests();

    // _shiftRequests = widget.shiftRequests;
  }
  Future<void> _fetchShiftRequests() async {
    final url = Uri.parse('$API_ENDPOINT/getOpenShiftRequests');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        List<dynamic> data = json.decode(response.body);
        setState(() {
          _shiftRequests = data.map((json) => ShiftRequest.fromJson(json)).toList();
        });
      } else {
        // Handle server error
        print('Server error: ${response.body}');
      }
    } catch (e) {
      // Handle network error
      print('Network error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;
    return Scaffold(
      backgroundColor: Colors.grey[850], // Dark background like CreateShiftRequestPage33
      appBar: AppBar(
        title: Text(
          'Open Shift Requests',
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

              colors: [Color(0xFF0f0f0f), Color(0xFF171717)], // Gradient colors

            ),
          ),
        ),
      ),
      body: Container(
        width: screenWidth,
        height: screenHeight,

        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            stops: [0.35, 0.90],
            tileMode: TileMode.repeated,

            colors: [Color(0xFF212224), Color(0xFF212224)],
          ),
        ),
        child: ListView.builder(
          itemCount: _shiftRequests.length,
          itemBuilder: (context, index) {
            return _buildShiftRequestItem(context, _shiftRequests[index]);
          },
        ),
      ),
    );
  }


  Widget _buildShiftRequestItem(BuildContext context, ShiftRequest request) {
    bool isSelected = _selectedRequest == request;
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return GestureDetector(
      onLongPressDown: (_) => setState(() => _selectedRequest = request),
      onLongPressUp: () => setState(() => _selectedRequest = null),
      onLongPress: () => _showCancelConfirmation(context, request),
      child: Card(
        color: const Color(0xFF1a1a1a),
        margin:EdgeInsets.symmetric(
        horizontal: screenWidth * 0.02, // 2% of screen width
        vertical: screenHeight * 0.01, // 1% of screen height
      ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(15),
        ),
        shadowColor: Color(0xFF820f09),
        elevation:0,
        child: InkWell(
          splashColor: Color(0xFF820f09),
          onTap: () {}, // Placeholder for tap functionality
          child: Column(
            children: [
              ListTile(
                contentPadding: EdgeInsets.symmetric(
                  horizontal: screenWidth * 0.05, // 5% of screen width
                  vertical: screenHeight * 0.01, // 1% of screen height
                ),                title: Text(
                  request.position,
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 22,
                    fontFamily: 'Proxima Nova',
                    color: Color(0xFFffffff),
                  ),
                ),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildRichText('Request ID: ', request.requestId.toString()), // Display requestId

                    _buildRichText('Date: ', _formatDate(request.date)),
                    _buildRichText('Time: ', '${_formatTime(request.fromTime)} - ${_formatTime(request.toTime)}'),
                    Divider(thickness: 1, indent: 0, endIndent: 0, color: Colors.black),

                    _buildRichText('Respond By: ', _formatDateTime(request.replyDeadline)),
                    _buildRichText('Current Bids: ', request.currentBids), // Display requestId

                  ],
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

  RichText _buildRichText(String label, String value) {
    return RichText(
      text: TextSpan(
        style: DefaultTextStyle.of(context).style,
        children: <TextSpan>[
          TextSpan(text: label, style: TextStyle(fontSize: 17,fontWeight: FontWeight.bold, color: Colors.white60,fontFamily: 'Proxima Nova',)),
          TextSpan(text: value, style: TextStyle(fontSize: 15,color: Colors.white,fontWeight: FontWeight.bold,fontFamily: 'Proxima Nova',)),
        ],
      ),
    );
  }
  String _formatDate(DateTime date) {
    return '${date.day.toString().padLeft(2, '0')}/${date.month.toString().padLeft(2, '0')}/${date.year}';
  }
  String _formatDateTime(DateTime dateTime) {
    return '${dateTime.day.toString().padLeft(2, '0')}/${dateTime.month.toString().padLeft(2, '0')}/${dateTime.year} ${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}';
  }

  String _formatTime(TimeOfDay time) {
    final hour = time.hour.toString().padLeft(2, '0');
    final minute = time.minute.toString().padLeft(2, '0');
    return '$hour:$minute';
  }




  void _cancelShiftRequest(String requestId) async {
    final url = Uri.parse('$API_ENDPOINT/getCancelShift');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'requestId': requestId}),
      );
      if (response.statusCode == 200) {
        // Handle successful cancellation
      } else {
        // Handle server error
      }
    } catch (e) {
      // Handle network error
    }
  }

  void _showCancelConfirmation(BuildContext context, ShiftRequest request) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Cancel Request'),
        content: Text('Are you sure you want to cancel this shift request for ${request.position}?'),        actions: <Widget>[
          TextButton(
            onPressed: () {
              _cancelShiftRequest(request.requestId); // Call the cancel function
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
        ),        ],
      ),
    );
  }

}
class ShiftRequest {
  final String position;
  final DateTime date;
  final TimeOfDay fromTime;
  final TimeOfDay toTime;
  final DateTime replyDeadline;
  final String requestId; // New field
  final String currentBids; // New field

  ShiftRequest({
    required this.position,
    required this.date,
    required this.fromTime,
    required this.toTime,
    required this.replyDeadline,
    required this.requestId, // Initialize in constructor
    required this.currentBids, // Initialize in constructor

  });

  factory ShiftRequest.fromJson(Map<String, dynamic> json) {
    // Helper function to parse TimeOfDay from a string.
    TimeOfDay? parseTime(String? timeString) {
      if (timeString == null) {
        return null;
      }
      final parts = timeString.split(':');
      if (parts.length != 2) {
        return null;
      }
      return TimeOfDay(hour: int.parse(parts[0]), minute: int.parse(parts[1]));
    }

    // Helper function to safely parse DateTime from a string.
    DateTime safeParseDateTime(String? dateTimeString) {
      try {
        return DateTime.parse(dateTimeString!);
      } catch (e) {
        return DateTime.now(); // default value in case of parsing error
      }
    }

    return ShiftRequest(
      position: json['position'] as String? ?? 'Unknown Position',
      date: safeParseDateTime(json['date']),
      fromTime: parseTime(json['fromTime']) ?? TimeOfDay(hour: 0, minute: 0),
      toTime: parseTime(json['toTime']) ?? TimeOfDay(hour: 0, minute: 0),
      replyDeadline: safeParseDateTime(json['replyDeadline']),
      requestId: json['requestID'] as String? ?? 'Unknown ID',
      currentBids: json['currentBids'] as String? ?? '0',

    );
  }




}


