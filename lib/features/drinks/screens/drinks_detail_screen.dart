import 'package:flutter/material.dart';

class DrinksDetailScreen extends StatelessWidget {
  const DrinksDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Drinks Detail'),
      ),
      body: const Center(
        child: Text('Drinks Detail Screen'),
      ),
    );
  }
}
