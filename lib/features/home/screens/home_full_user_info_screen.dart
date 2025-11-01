import 'package:flutter/material.dart';

class HomeFullUserInfoScreen extends StatelessWidget {
  const HomeFullUserInfoScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('User Information'),
      ),
      body: const Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Full Name: John Doe',
              style: TextStyle(fontSize: 18),
            ),
            SizedBox(height: 16),
            Text(
              'Email: john.doe@example.com',
              style: TextStyle(fontSize: 18),
            ),
            SizedBox(height: 16),
            Text(
              'Phone Number: +1 123 456 7890',
              style: TextStyle(fontSize: 18),
            ),
          ],
        ),
      ),
    );
  }
}
