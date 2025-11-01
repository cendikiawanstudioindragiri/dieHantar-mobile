import 'package:flutter/material.dart';

class DriverRatingScreen extends StatelessWidget {
  const DriverRatingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Driver Rating'),
      ),
      body: const Center(
        child: Text('Driver Rating Screen'),
      ),
    );
  }
}
