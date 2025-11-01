import 'package:flutter/material.dart';

class NotificationSearchEmptyScreen extends StatelessWidget {
  const NotificationSearchEmptyScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notification Search Empty'),
      ),
      body: const Center(
        child: Text('Notification Search Empty Screen'),
      ),
    );
  }
}
