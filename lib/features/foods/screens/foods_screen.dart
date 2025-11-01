import 'package:flutter/material.dart';

class FoodsScreen extends StatelessWidget {
  const FoodsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Foods'),
      ),
      body: const Center(
        child: Text('Foods Screen'),
      ),
    );
  }
}
