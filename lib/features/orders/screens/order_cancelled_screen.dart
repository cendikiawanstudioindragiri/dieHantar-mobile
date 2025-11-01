import 'package:flutter/material.dart';

class OrderCancelledScreen extends StatelessWidget {
  const OrderCancelledScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Cancelled Orders'),
      ),
      body: const Center(
        child: Text('Cancelled Orders Screen'),
      ),
    );
  }
}
