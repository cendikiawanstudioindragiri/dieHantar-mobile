import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class SettingPinSecurityScreen extends StatelessWidget {
  const SettingPinSecurityScreen({super.key});

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
              'You can use the PIN to unlock the app.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 32),
            const Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.circle_outlined, size: 24),
                SizedBox(width: 16),
                Icon(Icons.circle_outlined, size: 24),
                SizedBox(width: 16),
                Icon(Icons.circle_outlined, size: 24),
                SizedBox(width: 16),
                Icon(Icons.circle_outlined, size: 24),
              ],
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () => context.go('/setting-pin-security-scanning'),
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
