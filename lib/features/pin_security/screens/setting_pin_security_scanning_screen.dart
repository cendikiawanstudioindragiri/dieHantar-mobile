import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class SettingPinSecurityScanningScreen extends StatelessWidget {
  const SettingPinSecurityScanningScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Set Your PIN'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Spacer(),
            const Text(
              'Re-enter your PIN to confirm.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 32),
            const Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.circle, size: 24, color: Colors.blue),
                SizedBox(width: 16),
                Icon(Icons.circle, size: 24, color: Colors.blue),
                SizedBox(width: 16),
                Icon(Icons.circle, size: 24, color: Colors.blue),
                SizedBox(width: 16),
                Icon(Icons.circle_outlined, size: 24),
              ],
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () => context.go('/setting-pin-security-done'),
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 50),
              ),
              child: const Text('Continue'),
            ),
          ],
        ),
      ),
    );
  }
}
