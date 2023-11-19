import 'package:flutter/material.dart';

class CreateShiftRequestPage33 extends StatefulWidget {
  @override
  _CreateShiftRequestPageState createState() => _CreateShiftRequestPageState();
}

class _CreateShiftRequestPageState extends State<CreateShiftRequestPage33> {
  final _formKey = GlobalKey<FormState>();
  String _position = '';
  DateTime _selectedDate = DateTime.now();
  DateTime _replyDeadline = DateTime.now().add(Duration(days: 7));
  TimeOfDay? _selectedFromTime = TimeOfDay.now();
  TimeOfDay? _selectedToTime;

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Create Shift Request',
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
      body: Container(
        width: screenWidth,
        height: screenHeight,

        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            stops: [0.35, 0.90],
            tileMode: TileMode.repeated,

            colors: [Color(0xFF212121), Color(0xFF616161)],
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
                  _buildDateTimePicker('Selected Date', '${_selectedDate.toLocal().toString().split(' ')[0]}', () => _selectDate(context, true), screenWidth, screenHeight),
                  _buildTimePickerRow(screenWidth, screenHeight),
                  _buildDateTimePicker('Reply Deadline', '${_formatDateTime(_replyDeadline)}', () => _selectDateTime(context, false), screenWidth, screenHeight),
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
      padding: EdgeInsets.only(top: screenHeight * 0.01,bottom: screenHeight * 0.05),
      child: TextFormField(
        textAlign: TextAlign.left,
        style: TextStyle(
          fontSize: 18,
          color: Colors.white,
          fontWeight: FontWeight.bold,
          fontFamily: 'Proxima Nova',
        ),
        decoration: InputDecoration(
          labelText: label,
          labelStyle: TextStyle(
            color: Colors.white, // Example color
            fontSize: 16, // Example font size
            fontWeight: FontWeight.bold, // Example font weight
            fontFamily: 'Proxima Nova', // Example font family
          ),
          border: OutlineInputBorder(),
          contentPadding: EdgeInsets.symmetric(horizontal: screenWidth * 0.03, vertical: screenHeight * 0.01),
        ),
        onSaved: onSave,
        validator: (value) => value == null || value.isEmpty ? 'Please enter a $label' : null,
      ),
    );
  }


  Widget _buildDateTimePicker(String label, String value, VoidCallback onTap, double screenWidth, double screenHeight) {
    return Padding(
      padding: EdgeInsets.only(bottom: screenHeight * 0.05),
      child: InkWell(
        onTap: onTap,
        child: InputDecorator(
          decoration: InputDecoration(
            labelText: label,
            labelStyle: TextStyle(
              color: Colors.white, // Example color
              fontSize: 16, // Example font size
              fontWeight: FontWeight.bold, // Example font weight
              fontFamily: 'Proxima Nova', // Example font family
            ),
            border: OutlineInputBorder(),
            contentPadding: EdgeInsets.symmetric(horizontal: screenWidth * 0.03, vertical: screenHeight * 0.01),
          ),
          child: Text(
            value,
            textAlign: TextAlign.left,
            style: TextStyle(
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
      padding: EdgeInsets.symmetric(vertical: screenHeight * 0.03),
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.black,
          elevation: 5,
          alignment: Alignment.center,
          // textStyle: ,
          foregroundColor: Colors.red,
          // visualDensity:const VisualDensity(horizontal: .8,vertical: .8) ,
          shadowColor: Colors.deepPurple,

          padding: EdgeInsets.symmetric(horizontal: screenWidth * 0.2, vertical: screenHeight * 0.015),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(30),
          ),
        ),
        onPressed: () {
          // Rest of the code remains the same
        },
        child: const Text('Submit Request',
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
        title: Text('Shift Request Created'),
        content: Text('Position: $_position\nDate: ${_selectedDate.toLocal().toString().split(' ')[0]}\nFrom Time: ${_selectedFromTime?.format(context)}\nTo Time: ${_selectedToTime?.format(context)}\nReply Deadline: ${_replyDeadline.toLocal().toString().split(' ')[0]}'),
        actions: <Widget>[
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
            },
            child: Text('OK'),
          ),
        ],
      ),
    );
  }
  String _formatDateTime(DateTime dateTime) {
    // Format the DateTime into a string as per your requirements
    return '${dateTime.day.toString().padLeft(2, '0')}/${dateTime.month.toString().padLeft(2, '0')}/${dateTime.year} ${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}';
  }
  Future<void> _selectDateTime(BuildContext context, bool isShiftDate) async {
    // First, pick the date
    final DateTime? pickedDate = await showDatePicker(
      context: context,
      initialDate: isShiftDate ? _selectedDate : _replyDeadline,
      firstDate: DateTime.now(),
      lastDate: DateTime(2025),
    );

    if (pickedDate != null) {
      // If a date is picked, proceed to pick the time
      final TimeOfDay? pickedTime = await showTimePicker(
        context: context,
        initialTime: TimeOfDay.fromDateTime(isShiftDate ? _selectedDate : _replyDeadline),
      );

      if (pickedTime != null) {
        // Combine the picked date and time into a single DateTime
        final DateTime combinedDateTime = DateTime(
          pickedDate.year,
          pickedDate.month,
          pickedDate.day,
          pickedTime.hour,
          pickedTime.minute,
        );

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
      setState(() {
        if (isShiftDate) {
          _selectedDate = picked;
        } else {
          _replyDeadline = picked;
        }
      });
    }
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

}
