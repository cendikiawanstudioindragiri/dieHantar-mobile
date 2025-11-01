import 'package:flutter/material.dart';

class DrinksScreen extends StatelessWidget {
  const DrinksScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Drinks'),
      ),
      body: const Center(
        child: Text('Drinks Screen'),
      ),
    );
  }
}
