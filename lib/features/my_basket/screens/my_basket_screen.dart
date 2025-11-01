import 'package:flutter/material.dart';

class MyBasketScreen extends StatelessWidget {
  const MyBasketScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Basket'),
      ),
      body: const Center(
        child: Text('My Basket Screen'),
      ),
    );
  }
}
