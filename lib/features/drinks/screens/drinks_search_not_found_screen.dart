import 'package:flutter/material.dart';

class DrinksSearchNotFoundScreen extends StatelessWidget {
  const DrinksSearchNotFoundScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Drinks Search Not Found'),
      ),
      body: const Center(
        child: Text('Drinks Search Not Found Screen'),
      ),
    );
  }
}
