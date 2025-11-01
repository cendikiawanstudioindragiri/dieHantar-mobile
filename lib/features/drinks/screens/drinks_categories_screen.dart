import 'package:flutter/material.dart';

class DrinksCategoriesScreen extends StatelessWidget {
  const DrinksCategoriesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Drinks Categories'),
      ),
      body: const Center(
        child: Text('Drinks Categories Screen'),
      ),
    );
  }
}
