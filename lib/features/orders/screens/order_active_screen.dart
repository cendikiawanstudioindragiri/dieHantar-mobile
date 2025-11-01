import 'package:flutter/material.dart';

class OrderActiveScreen extends StatelessWidget {
  const OrderActiveScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Active Orders'),
      ),
      body: const Center(
        child: Text('Active Orders Screen'),
      ),
    );
  }
}
