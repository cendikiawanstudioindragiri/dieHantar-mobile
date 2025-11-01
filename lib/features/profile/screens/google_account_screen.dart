import 'package:flutter/material.dart';

class GoogleAccountScreen extends StatelessWidget {
  const GoogleAccountScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Google Account'),
      ),
      body: const Center(
        child: Text('Google Account Screen'),
      ),
    );
  }
}
