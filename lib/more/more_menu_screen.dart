import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class MoreMenuScreen extends StatelessWidget {
  const MoreMenuScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Lainnya'),
        backgroundColor: Colors.blueGrey,
      ),
      body: ListView(
        children: <Widget>[
          ListTile(
            leading: const Icon(Icons.person),
            title: const Text('Profil Pengguna'),
            subtitle: const Text('Ubah foto profil dan detail Anda'),
            trailing: const Icon(Icons.arrow_forward_ios),
            onTap: () {
              // Navigasi ke halaman profil yang telah kita buat
              context.go('/profile');
            },
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.security),
            title: const Text('Keamanan'),
            onTap: () {
              // TODO: Implement navigation to security settings
            },
          ),
          ListTile(
            leading: const Icon(Icons.notifications),
            title: const Text('Notifikasi'),
            onTap: () {
              // TODO: Implement navigation to notification settings
            },
          ),
          ListTile(
            leading: const Icon(Icons.star),
            title: const Text('Beri Rating'),
            onTap: () {
              // TODO: Implement navigation to rating screen
            },
          ),
        ],
      ),
    );
  }
}
