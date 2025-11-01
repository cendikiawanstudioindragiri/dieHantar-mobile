import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class LoginFilledScreen extends StatelessWidget {
  const LoginFilledScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextFormField(
              initialValue: 'email@example.com',
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.emailAddress,
            ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: 'password123',
              decoration: const InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () {
                // TODO: Implement login logic and navigate to home screen
                print('Login Successful!');
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 50),
              ),
              child: const Text('Login'),
            ),
            const SizedBox(height: 12),
            TextButton(
              onPressed: () => context.go('/signup-empty'),
              child: const Text('Don\'t have an account? Sign Up'),
            ),
            TextButton(
              onPressed: () => context.go('/forgot-password-empty'),
              child: const Text('Forgot Password?'),
            ),
          ],
        ),
      ),
    );
  }
}
