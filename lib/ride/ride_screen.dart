import 'package:flutter/material.dart';

class RideScreen extends StatelessWidget {
  const RideScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      appBar: AppBar(title: Text('dieHantar Ride')),
      body: Center(
        child: Text(
          'Layar untuk dieHantar Ride (Ojek & Taksi Online)',
          textAlign: TextAlign.center,
        ),
      ),
    );
  }
}
