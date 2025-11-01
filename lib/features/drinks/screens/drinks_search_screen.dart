import 'package:flutter/material.dart';

class DrinksSearchScreen extends StatelessWidget {
  const DrinksSearchScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Drinks Search'),
      ),
      body: const Center(
        child: Text('Drinks Search Screen'),
      ),
    );
  }
}
