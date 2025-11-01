import 'package:flutter/material.dart';

class LikedSearchScreen extends StatelessWidget {
  const LikedSearchScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Liked Search'),
      ),
      body: const Center(
        child: Text('Liked Search Screen'),
      ),
    );
  }
}
