import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:logging/logging.dart';


class AssignedShiftRequestsListPage extends StatefulWidget {

  const AssignedShiftRequestsListPage({Key? key}) : super(key: key);

  @override
  _ShiftRequestsListPageState createState() => _ShiftRequestsListPageState();
}

class _ShiftRequestsListPageState extends State<AssignedShiftRequestsListPage> {
  ShiftRequest? _selectedRequest;
  final Logger logger = Logger('ShiftRequestsLogger');
  List<ShiftRequest> _shiftRequests = [];

  Future<Map<String, dynamic>> loadConfig() async {
    final jsonString = await rootBundle.loadString('assets/config.json');
    return json.decode(jsonString);
  }
  Future<void> _fetchShiftRequests() async {
    final config = await loadConfig();
    final String apiEndpoint = config['api_endpoint'];
    final url = Uri.parse('$apiEndpoint/getScheduledShiftRequests');

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        logger.info("Successfully Fetched Assigned Shift Requests:");
        List<dynamic> data = json.decode(response.body);
        setState(() {
          _shiftRequests = data.map((json) => ShiftRequest.fromJson(json)).toList();
        });
      } else {
        logger.severe('Server error: ${response.body}');
        _showErrorDialog('Server error', 'Failed to fetch shift requests. Please try again later.');
      }
    } catch (e) {
      logger.severe('Network error: $e');
      _showErrorDialog('Network error', 'Failed to connect to the server. Please check your internet connection and try again.');
    }
  }

  void _showErrorDialog(String title, String message) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(title),
        content: Text(message),
        actions: <Widget>[
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
  @override
  void initState() {
    _fetchShiftRequests();

    super.initState();
  }
  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;
    return Scaffold(
      backgroundColor: Colors.grey[850],
      appBar: AppBar(
        title: const Text(
          'Assigned Shift Requests',
          textAlign: TextAlign.center,
          style: TextStyle(fontSize:22,color: Colors.white,fontWeight: FontWeight.bold,fontFamily:'Proxima Nova'),

        ),
        backgroundColor: Colors.deepPurple,
        elevation: 4,

        flexibleSpace: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              tileMode: TileMode.repeated,
              stops: [0.35, 0.90],

              colors: [Color(0xFF0f0f0f), Color(0xFF171717)],

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
      // onLongPress: () => _showCancelConfirmation(context, request),
      child: Card(
        color: const Color(0xFF1a1a1a),
        margin: EdgeInsets.symmetric(
          horizontal: screenWidth * 0.02,
          vertical: screenHeight * 0.01,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(15),
        ),
        shadowColor: const Color(0xFF820f09),
        elevation:0,
        child: InkWell(
          splashColor: const Color(0xFF820f09),
          child: Column(
            children: [
              ListTile(
          contentPadding: EdgeInsets.symmetric(
          horizontal: screenWidth * 0.05, // 5% of screen width
            vertical: screenHeight * 0.01, // 1% of screen height
          )  ,              title: Text(
                  request.position,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 22,
                    fontFamily: 'Proxima Nova',
                    color: Color(0xFFffffff),
                  ),
                ),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildRichText('Date: ', _formatDate(request.date)),
                    _buildRichText('Time: ', '${_formatTime(request.fromTime)} - ${_formatTime(request.toTime)}'),
                    const Divider(thickness: 1, indent: 0, endIndent: 0, color: Colors.black),
                    _buildRichText('Assigned To: ', request.assignedToName), // Assuming you have a property `assignedToName`
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
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

  String _formatTime(TimeOfDay time) {
    final hour = time.hour.toString().padLeft(2, '0');
    final minute = time.minute.toString().padLeft(2, '0');
    return '$hour:$minute';
  }





}
class ShiftRequest {
  final String position;
  final DateTime date;
  final TimeOfDay fromTime;
  final TimeOfDay toTime;
  final String assignedToName;

  ShiftRequest({
    required this.position,
    required this.date,
    required this.fromTime,
    required this.toTime,
    required this.assignedToName,

  });

  factory ShiftRequest.fromJson(Map<String, dynamic> json) {

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

    DateTime safeParseDateTime(String? dateTimeString) {
      try {
        return DateTime.parse(dateTimeString!);
      } catch (e) {
        return DateTime.now();
      }
    }

    return ShiftRequest(
      position: json['position'] as String? ?? 'Unknown Position',
      date: safeParseDateTime(json['date']),
      fromTime: parseTime(json['fromTime']) ?? const TimeOfDay(hour: 0, minute: 0),
      toTime: parseTime(json['toTime']) ?? const TimeOfDay(hour: 0, minute: 0),
      assignedToName: json['assignedToName'] as String? ?? '0',

    );
  }




}
