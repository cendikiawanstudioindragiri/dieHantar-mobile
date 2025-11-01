import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class IntroduceStep1Screen extends StatelessWidget {
  const IntroduceStep1Screen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Step 1'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Introduction Step 1'),
            ElevatedButton(
              onPressed: () => context.go('/introduce-step2'),
              child: const Text('Next'),
            ),
          ],
        ),
      ),
    );
  }
}
