import 'package:flutter/material.dart';

class DrinksAddBasketScreen extends StatelessWidget {
  const DrinksAddBasketScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Drinks Add Basket'),
      ),
      body: const Center(
        child: Text('Drinks Add Basket Screen'),
      ),
    );
  }
}
