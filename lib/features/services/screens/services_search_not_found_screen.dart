import 'package:flutter/material.dart';

class ServicesSearchNotFoundScreen extends StatelessWidget {
  const ServicesSearchNotFoundScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Services Search Not Found'),
      ),
      body: const Center(
        child: Text('Services Search Not Found Screen'),
      ),
    );
  }
}
