import 'package:flutter/material.dart';

class HelpCenterDetailScreen extends StatelessWidget {
  const HelpCenterDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Help Center Detail'),
      ),
      body: const Center(
        child: Text('Help Center Detail Screen'),
      ),
    );
  }
}
