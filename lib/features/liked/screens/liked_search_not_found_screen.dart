import 'package:flutter/material.dart';

class LikedSearchNotFoundScreen extends StatelessWidget {
  const LikedSearchNotFoundScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Liked Search Not Found'),
      ),
      body: const Center(
        child: Text('Liked Search Not Found Screen'),
      ),
    );
  }
}
