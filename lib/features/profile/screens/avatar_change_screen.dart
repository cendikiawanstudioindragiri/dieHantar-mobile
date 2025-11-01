import 'package:flutter/material.dart';

class AvatarChangeScreen extends StatelessWidget {
  const AvatarChangeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Avatar Change'),
      ),
      body: const Center(
        child: Text('Avatar Change Screen'),
      ),
    );
  }
}
