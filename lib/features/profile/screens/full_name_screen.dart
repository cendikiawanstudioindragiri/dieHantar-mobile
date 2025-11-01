import 'package:flutter/material.dart';

class FullNameScreen extends StatelessWidget {
  const FullNameScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Full Name'),
      ),
      body: const Center(
        child: Text('Full Name Screen'),
      ),
    );
  }
}
