import 'package:flutter/material.dart';

class DeliverySuccessfulScreen extends StatelessWidget {
  const DeliverySuccessfulScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Delivery Successful'),
      ),
      body: const Center(
        child: Text('Delivery Successful Screen'),
      ),
    );
  }
}
