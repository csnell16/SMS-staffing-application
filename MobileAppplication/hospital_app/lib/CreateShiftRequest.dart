import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:logging/logging.dart';

class CreateShiftRequestPage extends StatefulWidget {
  const CreateShiftRequestPage({super.key});

  @override
  _CreateShiftRequestPageState createState() => _CreateShiftRequestPageState();
}

class _CreateShiftRequestPageState extends State<CreateShiftRequestPage> {
  final _formKey = GlobalKey<FormState>();
  String _position = '';
  DateTime _selectedDate = DateTime.now();
  DateTime? _replyDeadline;
  TimeOfDay? _selectedFromTime = TimeOfDay.now();
  TimeOfDay? _selectedToTime;
  final Logger logger = Logger('CreateShiftRequestLogger');

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Create Shift Request',
          textAlign: TextAlign.center,
          style: TextStyle(fontSize:22,color: Colors.white,fontWeight: FontWeight.bold,fontFamily:'Proxima Nova'),

        ),
        elevation: 4,
        flexibleSpace: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              tileMode: TileMode.repeated,
              stops: [0.35, 0.85],

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
            stops: [0.35, 0.95],
            tileMode: TileMode.repeated,

            colors: [Color(0xFF212224), Color(0xFF212224)],
          ),
        ),
        child: SingleChildScrollView(
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: screenWidth * 0.04, vertical: screenHeight * 0.02),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: <Widget>[
                  _buildTextField('Position', (value) => _position = value!, screenWidth, screenHeight),
                  _buildDateTimePicker('Selected Date', _selectedDate.toLocal().toString().split(' ')[0], () => _selectDate(context, true), screenWidth, screenHeight),
                  _buildTimePickerRow(screenWidth, screenHeight),
                  _buildDateTimePicker(
                    'Respond By',
                    _replyDeadline != null ? _formatDateTime(_replyDeadline!) : 'Select Date and Time', // Display 'Not set' if null
                        () => _selectDateTime(context, false),
                    screenWidth,
                    screenHeight,
                  ),
                  _buildSubmitButton(screenWidth, screenHeight),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTextField(String label, Function(String?) onSave, double screenWidth, double screenHeight) {
    return Padding(
      padding: EdgeInsets.only(top: screenHeight * 0.02,bottom: screenHeight * 0.1),
      child: TextFormField(
        cursorColor: const Color(0xFF630f0b),
        textAlign: TextAlign.left,
        style: const TextStyle(
          fontSize: 19,
          color: Colors.white,
          fontWeight: FontWeight.bold,
          fontFamily: 'Proxima Nova',
        ),

        decoration: InputDecoration(

          enabledBorder: const OutlineInputBorder(
            borderSide: BorderSide(color: Colors.white),
          ),
          focusedBorder: const OutlineInputBorder(
            borderSide: BorderSide(color: Colors.white),
          ),
          labelText: label,
          labelStyle: const TextStyle(

            color: Colors.white,
            fontSize: 18,
            fontWeight: FontWeight.bold,
            fontFamily: 'Proxima Nova',
          ),
          border: const OutlineInputBorder(),
          contentPadding: EdgeInsets.symmetric(horizontal: screenWidth * 0.04, vertical: screenHeight * 0.03),
        ),
        onSaved: onSave,
        validator: (value) => value == null || value.isEmpty ? 'Please enter a $label' : null,

      ),
    );
  }


  Widget _buildDateTimePicker(String label, String value, VoidCallback onTap, double screenWidth, double screenHeight) {
    return Padding(
      padding: EdgeInsets.only(top: screenHeight * 0.01,bottom: screenHeight * 0.04),
      child: InkWell(
        onTap: onTap,
        child: InputDecorator(
          decoration: InputDecoration(
            labelText: label,
            labelStyle: const TextStyle(
              color: Colors.white, // Example color
              fontSize: 16, // Example font size
              fontWeight: FontWeight.bold, // Example font weight
              fontFamily: 'Proxima Nova', // Example font family
            ),
            border: const OutlineInputBorder(),
            contentPadding: EdgeInsets.symmetric(horizontal: screenWidth * 0.03, vertical: screenHeight * 0.01),
          ),
          child: Text(
            value,
            textAlign: TextAlign.left,
            style: const TextStyle(
              fontSize: 18,
              color: Colors.white,
              fontWeight: FontWeight.bold,
              fontFamily: 'Proxima Nova',
            ),
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ),
    );
  }



  Widget _buildTimePickerRow(double screenWidth, double screenHeight) {
    return Row(
      children: [
        Expanded(
          child: _buildDateTimePicker(
              'From Time',
              _selectedFromTime?.format(context) ?? 'Select Time',
                  () => _selectTime(context, true),
              screenWidth, screenHeight
          ),
        ),
        SizedBox(width: screenWidth * 0.02),
        Expanded(
          child: _buildDateTimePicker(
              'To Time',
              _selectedToTime?.format(context) ?? 'Select Time',
                  () => _selectTime(context, false),
              screenWidth, screenHeight
          ),
        ),
      ],
    );
  }

  Widget _buildSubmitButton(double screenWidth, double screenHeight) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: screenHeight * 0.1),
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFF0a0a0a),
          elevation: 0,
          alignment: Alignment.center,
          foregroundColor: const Color(0xFF820f09),
          // visualDensity:const VisualDensity(horizontal: .8,vertical: .8) ,
          // shadowColor: Color(0xFF820f09),

          padding: EdgeInsets.symmetric(horizontal: screenWidth * 0.2, vertical: screenHeight * 0.015),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(30),
          ),
        ),
        onPressed: () {
          logger.info("Submitted Request SMS sent");


          if (_formKey.currentState!.validate()) {
            _formKey.currentState!.save();
            _sendShiftRequest();
          }
        },
        child: const Text('Submit Request  ',
            textAlign: TextAlign.left,
          style: TextStyle(fontSize: 22,color: Color(0xFFFFFFFF),fontWeight: FontWeight.bold,fontFamily:'Proxima Nova'),
          overflow: TextOverflow.ellipsis,),
      ),
    );
  }

  void _showConfirmationDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Shift Request Created'),
        content: Text('Position: $_position\nDate: ${_selectedDate.toLocal().toString().split(' ')[0]}\nFrom Time: ${_selectedFromTime?.format(context)}\nTo Time: ${_selectedToTime?.format(context)}\nReply Deadline: ${_replyDeadline?.toLocal().toString().split(' ')[0]}'),
        actions: <Widget>[
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
            },
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
  String _formatDateTime(DateTime? dateTime) {
    if (dateTime == null) {
      return 'Select Date and Time';
    }
    return '${dateTime.day.toString().padLeft(2, '0')}/${dateTime.month.toString().padLeft(2, '0')}/${dateTime.year} ${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}';
  }
  Future<void> _selectDateTime(BuildContext context, bool isShiftDate) async {
    DateTime initialDate = isShiftDate ? _selectedDate : (_replyDeadline ?? DateTime.now());
    TimeOfDay initialTime = isShiftDate
        ? TimeOfDay.fromDateTime(_selectedDate)
        : (_replyDeadline != null ? TimeOfDay.fromDateTime(_replyDeadline!) : TimeOfDay.now());

    final DateTime? pickedDate = await showDatePicker(
      context: context,
      initialDate: initialDate,
      firstDate: DateTime.now(),
      lastDate: DateTime(2025),
    );

    if (pickedDate != null) {
      final TimeOfDay? pickedTime = await showTimePicker(
        context: context,
        initialTime: initialTime,
      );

      if (pickedTime != null) {
        final DateTime combinedDateTime = DateTime(
          pickedDate.year,
          pickedDate.month,
          pickedDate.day,
          pickedTime.hour,
          pickedTime.minute,
        );

        if (!isShiftDate && combinedDateTime.isAfter(_selectedDate)) {
          // Clear the reply deadline and show a warning message
          setState(() {
            _replyDeadline = null;
          });
          _showInvalidDateWarning();
          return;
        }

        setState(() {
          if (isShiftDate) {
            _selectedDate = combinedDateTime;
          } else {
            _replyDeadline = combinedDateTime;
          }
        });
      }
    }
  }

  _selectDate(BuildContext context, bool isShiftDate) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: isShiftDate ? _selectedDate : _replyDeadline,
      firstDate: DateTime.now(),
      lastDate: DateTime(2025),
    );
    if (picked != null) {
      if (!isShiftDate && picked.isAfter(_selectedDate)) {
        setState(() {
          _replyDeadline = null;
        });
        _showInvalidDateWarning();
        return;
      }
      setState(() {
        if (isShiftDate) {
          _selectedDate = picked;
        } else {
          _replyDeadline = picked;
        }
      });
    }
  }

  void _showInvalidDateWarning() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Invalid Date'),
        content: const Text('Reply deadline cannot be after the shift start time.'),
        actions: <Widget>[
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
            },
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }


  _selectTime(BuildContext context, bool isFromTime) async {
    final initialTime = isFromTime
        ? (_selectedFromTime ?? TimeOfDay.now())
        : (_selectedToTime ?? TimeOfDay.now());

    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: initialTime,
    );

    if (picked != null) {
      setState(() {
        if (isFromTime) {
          _selectedFromTime = picked;
        } else {
          _selectedToTime = picked;
        }
      });
    }
  }
  Future<Map<String, dynamic>> loadConfig() async {
    final jsonString = await rootBundle.loadString('assets/config.json');
    return json.decode(jsonString);
  }
  Future<void> _sendShiftRequest() async {
    final config = await loadConfig();
    final String apiEndpoint = config['api_endpoint'];

    final url = Uri.parse('$apiEndpoint/shiftCreation');
    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: json.encode({
          'position': _position,
          'selectedDate': _selectedDate.toIso8601String(),
          'fromTime': _selectedFromTime?.format(context),
          'toTime': _selectedToTime?.format(context),
          'replyDeadline': _replyDeadline?.toIso8601String(),

        }),
      );

      if (response.statusCode == 200) {
        logger.info("Successfully Created Shift Request");
        _showConfirmationDialog();
      } else {
        logger.severe('Server error: ${response.body}');
        _showErrorDialog('Server error', 'Failed to fetch shift requests. Please try again later.');
      }
    }
    catch (e) {
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


}
