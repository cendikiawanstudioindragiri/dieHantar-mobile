import 'package:flutter/material.dart';

class PaymentAddNewCardFilledScreen extends StatelessWidget {
  const PaymentAddNewCardFilledScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Card Filled'),
      ),
      body: const Center(
        child: Text('Card Filled Screen'),
      ),
    );
  }
}
