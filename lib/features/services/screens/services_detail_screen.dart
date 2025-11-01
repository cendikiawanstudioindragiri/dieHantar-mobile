import 'package:flutter/material.dart';

class ServicesDetailScreen extends StatelessWidget {
  const ServicesDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Services Detail'),
      ),
      body: const Center(
        child: Text('Services Detail Screen'),
      ),
    );
  }
}
