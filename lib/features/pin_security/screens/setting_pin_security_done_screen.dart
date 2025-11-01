import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class SettingPinSecurityDoneScreen extends StatelessWidget {
  const SettingPinSecurityDoneScreen({super.key});

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
            const Icon(
              Icons.check_circle,
              size: 150,
              color: Colors.green,
            ),
            const SizedBox(height: 16),
            const Text(
              'PIN has been set successfully!',
              style: TextStyle(color: Colors.green, fontSize: 18),
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () => context.go('/'), // Navigate to home or next screen
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 50),
              ),
              child: const Text('Done'),
            ),
          ],
        ),
      ),
    );
  }
}
