import 'package:flutter/material.dart';

class OrderNotFoundScreen extends StatelessWidget {
  const OrderNotFoundScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Order Not Found'),
      ),
      body: const Center(
        child: Text('Order Not Found Screen'),
      ),
    );
  }
}
