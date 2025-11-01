import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class LoadingStartScreen extends StatelessWidget {
  const LoadingStartScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Navigate to the next screen after a delay
    Future.delayed(const Duration(seconds: 2), () {
      context.go('/loading-middle');
    });

    return const Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(),
            SizedBox(height: 20),
            Text('Loading...'),
          ],
        ),
      ),
    );
  }
}
