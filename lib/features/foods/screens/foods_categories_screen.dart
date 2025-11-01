import 'package:flutter/material.dart';

class FoodsCategoriesScreen extends StatelessWidget {
  const FoodsCategoriesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Foods Categories'),
      ),
      body: const Center(
        child: Text('Foods Categories Screen'),
      ),
    );
  }
}
