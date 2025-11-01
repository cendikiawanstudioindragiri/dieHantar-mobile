import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class IntroduceStep2Screen extends StatelessWidget {
  const IntroduceStep2Screen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Step 2'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Introduction Step 2'),
            ElevatedButton(
              onPressed: () => context.go('/introduce-step3'),
              child: const Text('Next'),
            ),
          ],
        ),
      ),
    );
  }
}
