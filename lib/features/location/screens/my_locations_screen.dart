import 'package:flutter/material.dart';

class MyLocationsScreen extends StatelessWidget {
  const MyLocationsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Locations'),
      ),
      body: const Center(
        child: Text('My Locations Screen'),
      ),
    );
  }
}
