import 'package:flutter/material.dart';

class FeedbackScreen extends StatelessWidget {
  const FeedbackScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Input and Suggestions'),
      ),
      body: const Center(
        child: Text('Input and Suggestions Screen'),
      ),
    );
  }
}
