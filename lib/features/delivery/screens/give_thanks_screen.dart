import 'package:flutter/material.dart';

class GiveThanksScreen extends StatelessWidget {
  const GiveThanksScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Give Thanks'),
      ),
      body: const Center(
        child: Text('Give Thanks Screen'),
      ),
    );
  }
}
