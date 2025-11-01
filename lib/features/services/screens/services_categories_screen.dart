import 'package:flutter/material.dart';

class ServicesCategoriesScreen extends StatelessWidget {
  const ServicesCategoriesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Services Categories'),
      ),
      body: const Center(
        child: Text('Services Categories Screen'),
      ),
    );
  }
}
