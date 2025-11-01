import 'package:flutter/material.dart';

class PaymentCheckedScreen extends StatelessWidget {
  const PaymentCheckedScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Payment Checked'),
      ),
      body: const Center(
        child: Text('Payment Checked Screen'),
      ),
    );
  }
}
