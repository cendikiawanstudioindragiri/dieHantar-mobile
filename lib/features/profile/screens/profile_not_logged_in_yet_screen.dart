import 'package:flutter/material.dart';

class ProfileNotLoggedInYetScreen extends StatelessWidget {
  const ProfileNotLoggedInYetScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Not Logged In Yet'),
      ),
      body: const Center(
        child: Text('Not Logged In Yet Screen'),
      ),
    );
  }
}
