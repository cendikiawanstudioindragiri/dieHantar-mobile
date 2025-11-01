import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class SettingTouchIdScanningScreen extends StatelessWidget {
  const SettingTouchIdScanningScreen({super.key});

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
              'Place your finger on the fingerprint scanner to get started.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 32),
            const Icon(
              Icons.fingerprint,
              size: 150,
              color: Colors.blue, // Simulating scanning
            ),
            const SizedBox(height: 16),
            const Text(
              'Scanning...',
              style: TextStyle(color: Colors.blue, fontSize: 16),
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () => context.go('/setting-touch-id-done'),
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
