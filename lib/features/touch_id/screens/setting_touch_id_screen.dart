import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class SettingTouchIdScreen extends StatelessWidget {
  const SettingTouchIdScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Set Your Touch ID'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Spacer(),
            const Text(
              'Add your fingerprint to make your account more secure.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 32),
            const Icon(
              Icons.fingerprint,
              size: 150,
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () => context.go('/setting-touch-id-scanning'),
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 50),
              ),
              child: const Text('Continue'),
            ),
            const SizedBox(height: 16),
            TextButton(
              onPressed: () {},
              child: const Text('Skip'),
            ),
          ],
        ),
      ),
    );
  }
}
