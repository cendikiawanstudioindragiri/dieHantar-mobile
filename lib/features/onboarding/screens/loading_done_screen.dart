import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class LoadingDoneScreen extends StatelessWidget {
  const LoadingDoneScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Navigate to the next screen after a delay
    Future.delayed(const Duration(seconds: 2), () {
      context.go('/welcome');
    });

    return const Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.check_circle, color: Colors.green, size: 50),
            SizedBox(height: 20),
            Text('Loading complete!'),
          ],
        ),
      ),
    );
  }
}
