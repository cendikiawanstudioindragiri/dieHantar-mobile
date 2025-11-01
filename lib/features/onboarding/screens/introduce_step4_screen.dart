import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class IntroduceStep4Screen extends StatelessWidget {
  const IntroduceStep4Screen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Step 4'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Introduction Step 4'),
            ElevatedButton(
              onPressed: () => context.go('/login-empty'),
              child: const Text('Finish'),
            ),
          ],
        ),
      ),
    );
  }
}
