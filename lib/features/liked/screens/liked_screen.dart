import 'package:flutter/material.dart';

class LikedScreen extends StatelessWidget {
  const LikedScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Liked'),
      ),
      body: const Center(
        child: Text('Liked Screen'),
      ),
    );
  }
}
