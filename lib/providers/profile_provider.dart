import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/image_upload_service.dart';

class ProfileProvider with ChangeNotifier {
  final ImageUploadService _imageUploadService = ImageUploadService();

  String? _profileImageUrl;
  String? get profileImageUrl => _profileImageUrl;

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  static const String _profileImageKey = 'profile_image_url';

  ProfileProvider() {
    // Muat URL gambar yang tersimpan saat provider diinisialisasi
    _loadProfileImageUrl();
  }

  // Memuat URL gambar dari penyimpanan lokal
  Future<void> _loadProfileImageUrl() async {
    final prefs = await SharedPreferences.getInstance();
    _profileImageUrl = prefs.getString(_profileImageKey);
    notifyListeners();
  }

  // Menyimpan URL gambar ke penyimpanan lokal
  Future<void> _saveProfileImageUrl(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_profileImageKey, url);
  }

  // Fungsi utama untuk memilih dan mengunggah gambar
  Future<void> uploadProfilePicture() async {
    _setLoading(true);

    try {
      final String? newImageUrl = await _imageUploadService.pickAndUploadImage();

      if (newImageUrl != null) {
        _profileImageUrl = newImageUrl;
        // Simpan URL baru ke penyimpanan lokal agar tetap ada saat aplikasi dibuka kembali
        await _saveProfileImageUrl(newImageUrl);
      }
      // Jika newImageUrl null, artinya pengguna membatalkan pemilihan,
      // jadi kita tidak perlu melakukan apa-apa.
    } catch (e) {
      // Tangani kemungkinan error lain dari service
      print("Error di ProfileProvider: $e");
    }

    _setLoading(false);
  }

  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }
}
