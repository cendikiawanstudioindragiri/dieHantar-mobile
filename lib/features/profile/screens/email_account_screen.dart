import 'package:flutter/material.dart';

class EmailAccountScreen extends StatelessWidget {
  const EmailAccountScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Email Account'),
      ),
      body: const Center(
        child: Text('Email Account Screen'),
      ),
    );
  }
}
