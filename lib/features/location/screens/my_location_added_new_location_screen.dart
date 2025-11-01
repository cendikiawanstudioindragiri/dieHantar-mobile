import 'package:flutter/material.dart';

class MyLocationAddedNewLocationScreen extends StatelessWidget {
  const MyLocationAddedNewLocationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Added New Location'),
      ),
      body: const Center(
        child: Text('Added New Location Screen'),
      ),
    );
  }
}
