import 'package:flutter/material.dart';

class OrdersActiveDetailScreen extends StatelessWidget {
  const OrdersActiveDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Active Order Detail'),
      ),
      body: const Center(
        child: Text('Active Order Detail Screen'),
      ),
    );
  }
}
