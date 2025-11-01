import 'package:flutter/material.dart';

class CallingScreen extends StatelessWidget {
  const CallingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Calling'),
      ),
      body: const Center(
        child: Text('Calling Screen'),
      ),
    );
  }
}
