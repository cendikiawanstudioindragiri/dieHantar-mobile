import 'package:flutter/material.dart';

class PaymentAddNewCardScreen extends StatelessWidget {
  const PaymentAddNewCardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add New Card'),
      ),
      body: const Center(
        child: Text('Add New Card Screen'),
      ),
    );
  }
}
