import 'package:flutter/material.dart';

class CancelOrderScreen extends StatelessWidget {
  const CancelOrderScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Cancel Order'),
      ),
      body: const Center(
        child: Text('Cancel Order Screen'),
      ),
    );
  }
}
