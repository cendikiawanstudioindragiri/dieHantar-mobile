import 'package:flutter/material.dart';

class PaymentScanQrisMethodScreen extends StatelessWidget {
  const PaymentScanQrisMethodScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Scan QRIS'),
      ),
      body: const Center(
        child: Text('Scan QRIS Screen'),
      ),
    );
  }
}
