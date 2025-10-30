
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:myapp/app/auth/auth_repository.dart';
import 'package:myapp/app/settings/settings_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final authRepository = AuthRepository(FirebaseService());
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (context) => const SettingsScreen(),
                ),
              );
            },
          ),
        ],
      ),
      body: StreamBuilder<User?>(
        stream: authRepository.currentUser as Stream<User?>?,
        builder: (context, snapshot) {
          final user = snapshot.data;
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                if (user?.photoURL != null)
                  CircleAvatar(
                    radius: 50,
                    backgroundImage: NetworkImage(user!.photoURL!),
                  ),
                const SizedBox(height: 20),
                Text('Welcome, ${user?.displayName ?? 'User'}!'),
                const SizedBox(height: 20),
                ElevatedButton(
                  child: const Text('Sign out'),
                  onPressed: () => authRepository.signOut(),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}

class FirebaseService {
}
