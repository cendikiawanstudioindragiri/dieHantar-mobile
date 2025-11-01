import 'package:flutter/material.dart';

class PaymentPaymentSuccessScreen extends StatelessWidget {
  const PaymentPaymentSuccessScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Payment Success'),
      ),
      body: const Center(
        child: Text('Payment Success Screen'),
      ),
    );
  }
}
