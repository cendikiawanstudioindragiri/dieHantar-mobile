import 'package:flutter/material.dart';

class FoodsDetailSelectScreen extends StatelessWidget {
  const FoodsDetailSelectScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Foods Detail Select'),
      ),
      body: const Center(
        child: Text('Foods Detail Select Screen'),
      ),
    );
  }
}
