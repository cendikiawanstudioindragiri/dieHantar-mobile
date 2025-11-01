import 'package:flutter/material.dart';

class SendScreen extends StatelessWidget {
  const SendScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      appBar: AppBar(title: Text('dieHantar Send')),
      body: Center(
        child: Text(
          'Layar untuk dieHantar Send (Kurir Instan)',
          textAlign: TextAlign.center,
        ),
      ),
    );
  }
}
