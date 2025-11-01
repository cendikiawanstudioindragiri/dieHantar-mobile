import 'package:flutter/material.dart';

class RateYourMealScreen extends StatelessWidget {
  const RateYourMealScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Rate Your Meal'),
      ),
      body: const Center(
        child: Text('Rate Your Meal Screen'),
      ),
    );
  }
}
