import 'package:flutter/material.dart';

class DriverInformationScreen extends StatelessWidget {
  const DriverInformationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Driver Information'),
      ),
      body: const Center(
        child: Text('Driver Information Screen'),
      ),
    );
  }
}
