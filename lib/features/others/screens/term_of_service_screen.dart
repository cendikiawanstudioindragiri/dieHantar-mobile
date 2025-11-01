import 'package:flutter/material.dart';

class TermOfServiceScreen extends StatelessWidget {
  const TermOfServiceScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Term of Service'),
      ),
      body: const Center(
        child: Text('Term of Service Screen'),
      ),
    );
  }
}
