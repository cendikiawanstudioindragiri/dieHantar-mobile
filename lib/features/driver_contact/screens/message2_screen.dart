import 'package:flutter/material.dart';

class Message2Screen extends StatelessWidget {
  const Message2Screen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Message 2'),
      ),
      body: const Center(
        child: Text('Message 2 Screen'),
      ),
    );
  }
}
