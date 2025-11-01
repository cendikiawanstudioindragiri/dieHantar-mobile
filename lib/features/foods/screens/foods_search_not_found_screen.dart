import 'package:flutter/material.dart';

class FoodsSearchNotFoundScreen extends StatelessWidget {
  const FoodsSearchNotFoundScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Foods Search Not Found'),
      ),
      body: const Center(
        child: Text('Foods Search Not Found Screen'),
      ),
    );
  }
}
