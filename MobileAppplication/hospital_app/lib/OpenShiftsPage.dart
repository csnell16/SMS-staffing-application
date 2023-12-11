import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:logging/logging.dart';


class OpenShiftsListPage extends StatefulWidget {

  const OpenShiftsListPage({Key? key}) : super(key: key);

  @override
  _OpenShiftsListPageState createState() => _OpenShiftsListPageState();
}

class _OpenShiftsListPageState extends State<OpenShiftsListPage> {
  ShiftRequest? _selectedRequest;
  final Logger logger = Logger('OpenShiftsListPageLogger');


  List<ShiftRequest> _shiftRequests = [];

  @override
  void initState() {
    super.initState();
    _fetchShiftRequests();
  }
  Future<Map<String, dynamic>> loadConfig() async {
    final jsonString = await rootBundle.loadString('assets/config.json');
    return json.decode(jsonString);
  }
  Future<void> _fetchShiftRequests() async {
    final config = await loadConfig();
    final String apiEndpoint = config['api_endpoint'];
    final url = Uri.parse('$apiEndpoint/getOpenShiftRequests');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        logger.info("Successfully Fetched Shift Requests:");
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
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;
    return Scaffold(
      backgroundColor: Colors.grey[850],
      appBar: AppBar(
        title: const Text(
          'Open Shift Requests',
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

              colors: [Color(0xFF0f0f0f), Color(0xFF171717)], // Gradient colors

            ),
          ),
        ),
      ),
      body: Container(
        width: screenWidth,
        height: screenHeight,

        decoration: const BoxDecoration(
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
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return GestureDetector(
      onLongPressDown: (_) => setState(() => _selectedRequest = request),
      onLongPressUp: () => setState(() => _selectedRequest = null),
      onLongPress: () => _showCancelConfirmation(context, request),
      child: Card(
        color: const Color(0xFF1a1a1a),
        margin:EdgeInsets.symmetric(
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
                  horizontal: screenWidth * 0.05,
                  vertical: screenHeight * 0.01,
                ),                title: Text(
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
                    _buildRichText('Request ID: ', request.requestId.toString()),

                    _buildRichText('Date: ', _formatDate(request.date)),
                    _buildRichText('Time: ', '${_formatTime(request.fromTime)} - ${_formatTime(request.toTime)}'),
                    const Divider(thickness: 1, indent: 0, endIndent: 0, color: Colors.black),

                    _buildRichText('Respond By: ', _formatDateTime(request.replyDeadline)),
                    _buildRichText('Current Bids: ', request.currentBids),

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
          TextSpan(text: label, style: const TextStyle(fontSize: 17,fontWeight: FontWeight.bold, color: Colors.white60,fontFamily: 'Proxima Nova',)),
          TextSpan(text: value, style: const TextStyle(fontSize: 15,color: Colors.white,fontWeight: FontWeight.bold,fontFamily: 'Proxima Nova',)),
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
    final config = await loadConfig();
    final String apiEndpoint = config['api_endpoint'];
    final url = Uri.parse('$apiEndpoint/getCancelShift');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'requestId': requestId}),
      );
      if (response.statusCode == 200) {
        logger.info("Successfully Canceled Shift Request: $requestId");

        _showErrorDialog('Successfully Canceled Shift Request: $requestId', '');
      }
      else {
      logger.severe('Server error: ${response.body}');
      _showErrorDialog('Server error', 'Failed to cancel shift requests. Please try again later.');
     }
    }
   catch (e) {
    logger.severe('Network error: $e');
    _showErrorDialog('Network error', 'Failed to connect to the server. Please check your internet connection and try again.');

   }
  }

  void _showCancelConfirmation(BuildContext context, ShiftRequest request) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Cancel Request'),
        content: Text('Are you sure you want to cancel this shift request for ${request.position}?'), actions: <Widget>[
          TextButton(
            onPressed: () {
              _cancelShiftRequest(request.requestId);
              setState(() {
                _shiftRequests.remove(request);
              });
              Navigator.of(context).pop();
            },
            child: const Text('Yes', style: TextStyle(color: Colors.red)),
          ),
        TextButton(
          onPressed: () {
            Navigator.of(context).pop();
          },
          child: const Text('No'),
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
  final String requestId;
  final String currentBids;

  ShiftRequest({
    required this.position,
    required this.date,
    required this.fromTime,
    required this.toTime,
    required this.replyDeadline,
    required this.requestId,
    required this.currentBids,

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
      fromTime: parseTime(json['fromTime']) ?? TimeOfDay(hour: 0, minute: 0),
      toTime: parseTime(json['toTime']) ??  TimeOfDay(hour: 0, minute: 0),
      replyDeadline: safeParseDateTime(json['replyDeadline']),
      requestId: json['requestID'] as String? ?? 'Unknown ID',
      currentBids: json['currentBids'] as String? ?? '0',

    );
  }




}


