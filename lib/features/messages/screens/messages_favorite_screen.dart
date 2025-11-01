import 'package:flutter/material.dart';

class MessagesFavoriteScreen extends StatelessWidget {
  const MessagesFavoriteScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Favorite Messages'),
      ),
      body: const Center(
        child: Text('Favorite Messages Screen'),
      ),
    );
  }
}
