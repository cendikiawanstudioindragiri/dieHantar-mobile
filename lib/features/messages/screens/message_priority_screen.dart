import 'package:flutter/material.dart';

class MessagePriorityScreen extends StatelessWidget {
  const MessagePriorityScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Priority Messages'),
      ),
      body: const Center(
        child: Text('Priority Messages Screen'),
      ),
    );
  }
}
