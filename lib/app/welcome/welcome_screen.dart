import 'package:flutter/material.dart';
import 'package:myapp/app/auth/auth_repository.dart';
import 'package:myapp/app/auth/login_screen.dart';
import 'package:myapp/signup/signup_screen.dart';
import 'package:provider/provider.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Get the AuthRepository from the Provider
    final authRepository = Provider.of<AuthRepository>(context);

    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                'Selamat Datang',
                style: Theme.of(context).textTheme.displayLarge,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              Text(
                'Mulai perjalanan Anda dengan Cendikiawan Studios',
                style: Theme.of(context).textTheme.titleMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 48),
              ElevatedButton.icon(
                icon: const Icon(
                  Icons.g_mobiledata,
                ), // Placeholder for Google Icon
                label: const Text('Masuk dengan Google'),
                onPressed: () async {
                  final user = await authRepository.signInWithGoogle();
                  if (user != null) {
                    // Navigate to home screen on successful login
                    // You might want to use go_router for this
                  } else {
                    // Handle sign-in failure
                    if (!context.mounted) return;
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('Gagal masuk dengan Google.'),
                      ),
                    );
                  }
                },
              ),
              const SizedBox(height: 16),
              OutlinedButton(
                child: const Text('Daftar dengan Email'),
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => const SignupScreen(),
                    ),
                  );
                },
              ),
              const SizedBox(height: 16),
              TextButton(
                child: const Text('Sudah punya akun? Masuk'),
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => const LoginScreen(),
                    ),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
