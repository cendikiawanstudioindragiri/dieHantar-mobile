import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class IntroduceStep3Screen extends StatelessWidget {
  const IntroduceStep3Screen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Step 3'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Introduction Step 3'),
            ElevatedButton(
              onPressed: () => context.go('/introduce-step4'),
              child: const Text('Next'),
            ),
          ],
        ),
      ),
    );
  }
}
