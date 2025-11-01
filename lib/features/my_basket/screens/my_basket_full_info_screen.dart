import 'package:flutter/material.dart';

class MyBasketFullInfoScreen extends StatelessWidget {
  const MyBasketFullInfoScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Basket Full Info'),
      ),
      body: const Center(
        child: Text('My Basket Full Info Screen'),
      ),
    );
  }
}
