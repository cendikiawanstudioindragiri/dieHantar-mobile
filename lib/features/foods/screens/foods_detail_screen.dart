import 'package:flutter/material.dart';

class FoodsDetailScreen extends StatelessWidget {
  const FoodsDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Foods Detail'),
      ),
      body: const Center(
        child: Text('Foods Detail Screen'),
      ),
    );
  }
}
