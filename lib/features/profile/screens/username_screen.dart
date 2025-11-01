import 'package:flutter/material.dart';

class UsernameScreen extends StatelessWidget {
  const UsernameScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Username'),
      ),
      body: const Center(
        child: Text('Username changes can only be made after 30 days.'),
      ),
    );
  }
}
