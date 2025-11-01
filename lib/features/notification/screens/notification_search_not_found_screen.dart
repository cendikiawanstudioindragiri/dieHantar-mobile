import 'package:flutter/material.dart';

class NotificationSearchNotFoundScreen extends StatelessWidget {
  const NotificationSearchNotFoundScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notification Search Not Found'),
      ),
      body: const Center(
        child: Text('Notification Search Not Found Screen'),
      ),
    );
  }
}
