import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/profile_provider.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profil Pengguna'),
        backgroundColor: Colors.indigo,
      ),
      body: Center(
        child: Consumer<ProfileProvider>(
          builder: (context, provider, child) {
            return Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                // --- Avatar Gambar Profil ---
                GestureDetector(
                  onTap: () => provider.uploadProfilePicture(),
                  child: CircleAvatar(
                    radius: 80,
                    backgroundColor: Colors.grey[300],
                    backgroundImage: provider.profileImageUrl != null
                        ? NetworkImage(provider.profileImageUrl!)
                        : null,
                    child: provider.isLoading
                        ? const CircularProgressIndicator() // Tampilkan loading di dalam avatar
                        : provider.profileImageUrl == null
                            ? Icon(
                                Icons.camera_alt,
                                color: Colors.grey[800],
                                size: 50,
                              )
                            : null,
                  ),
                ),
                const SizedBox(height: 20),

                // --- Teks Nama Pengguna (Placeholder) ---
                const Text(
                  'Nama Pengguna', 
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 10),
                const Text(
                  'email@contoh.com', 
                  style: TextStyle(fontSize: 16, color: Colors.grey),
                ),

                const SizedBox(height: 40),

                // --- Tombol untuk Mengunggah/Mengubah Gambar ---
                ElevatedButton.icon(
                  onPressed: provider.isLoading ? null : () => provider.uploadProfilePicture(),
                  icon: const Icon(Icons.upload_file),
                  label: const Text('Ubah Foto Profil'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.indigo,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                  ),
                ),
                
                // Pesan status (opsional)
                if (provider.isLoading)
                  const Padding(
                    padding: EdgeInsets.only(top: 20),
                    child: Text("Mengunggah gambar..."),
                  ),
              ],
            );
          },
        ),
      ),
    );
  }
}
