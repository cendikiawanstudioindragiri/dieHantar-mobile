import 'package:flutter/material.dart';

class MyLocationAddNewLocationScreen extends StatelessWidget {
  const MyLocationAddNewLocationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add New Location'),
      ),
      body: const Center(
        child: Text('Add New Location Screen'),
      ),
    );
  }
}
