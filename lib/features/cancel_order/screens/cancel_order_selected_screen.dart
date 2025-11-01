import 'package:flutter/material.dart';

class CancelOrderSelectedScreen extends StatelessWidget {
  const CancelOrderSelectedScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Cancel Order Selected'),
      ),
      body: const Center(
        child: Text('Cancel Order Selected Screen'),
      ),
    );
  }
}
