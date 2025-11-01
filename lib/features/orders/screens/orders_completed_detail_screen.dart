import 'package:flutter/material.dart';

class OrdersCompletedDetailScreen extends StatelessWidget {
  const OrdersCompletedDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Completed Order Detail'),
      ),
      body: const Center(
        child: Text('Completed Order Detail Screen'),
      ),
    );
  }
}
