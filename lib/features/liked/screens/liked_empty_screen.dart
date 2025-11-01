import 'package:flutter/material.dart';

class LikedEmptyScreen extends StatelessWidget {
  const LikedEmptyScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Liked Empty'),
      ),
      body: const Center(
        child: Text('Liked Empty Screen'),
      ),
    );
  }
}
