import 'package:flutter/material.dart';

class ServicesSearchScreen extends StatelessWidget {
  const ServicesSearchScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Services Search'),
      ),
      body: const Center(
        child: Text('Services Search Screen'),
      ),
    );
  }
}
