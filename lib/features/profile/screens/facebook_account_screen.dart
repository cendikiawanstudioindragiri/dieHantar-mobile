import 'package:flutter/material.dart';

class FacebookAccountScreen extends StatelessWidget {
  const FacebookAccountScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Facebook Account'),
      ),
      body: const Center(
        child: Text('Facebook Account Screen'),
      ),
    );
  }
}
