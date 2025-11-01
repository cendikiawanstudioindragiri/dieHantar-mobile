import 'package:flutter/material.dart';

class MyLocationsFavoriteScreen extends StatelessWidget {
  const MyLocationsFavoriteScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Favorite Locations'),
      ),
      body: const Center(
        child: Text('Favorite Locations Screen'),
      ),
    );
  }
}
