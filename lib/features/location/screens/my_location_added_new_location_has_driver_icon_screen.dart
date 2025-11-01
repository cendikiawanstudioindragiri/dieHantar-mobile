import 'package:flutter/material.dart';

class MyLocationAddedNewLocationHasDriverIconScreen extends StatelessWidget {
  const MyLocationAddedNewLocationHasDriverIconScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Added New Location'),
        actions: [
          IconButton(
            icon: const Icon(Icons.drive_eta),
            onPressed: () {},
          ),
        ],
      ),
      body: const Center(
        child: Text('Added New Location Screen'),
      ),
    );
  }
}
