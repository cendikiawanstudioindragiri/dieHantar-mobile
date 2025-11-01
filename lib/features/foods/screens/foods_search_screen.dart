import 'package:flutter/material.dart';

class FoodsSearchScreen extends StatelessWidget {
  const FoodsSearchScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Foods Search'),
      ),
      body: const Center(
        child: Text('Foods Search Screen'),
      ),
    );
  }
}
