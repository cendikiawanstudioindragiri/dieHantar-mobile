import 'package:flutter/material.dart';

class PhoneNumberAccountScreen extends StatelessWidget {
  const PhoneNumberAccountScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Phone Number Account'),
      ),
      body: const Center(
        child: Text('Phone Number Account Screen'),
      ),
    );
  }
}
