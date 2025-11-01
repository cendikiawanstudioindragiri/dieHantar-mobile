import 'package:flutter/material.dart';

class OrdersCancelledDetailScreen extends StatelessWidget {
  const OrdersCancelledDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Cancelled Order Detail'),
      ),
      body: const Center(
        child: Text('Cancelled Order Detail Screen'),
      ),
    );
  }
}
