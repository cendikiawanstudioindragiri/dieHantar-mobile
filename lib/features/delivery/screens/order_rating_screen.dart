import 'package:flutter/material.dart';

class OrderRatingScreen extends StatelessWidget {
  const OrderRatingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Order Rating'),
      ),
      body: const Center(
        child: Text('Order Rating Screen'),
      ),
    );
  }
}
