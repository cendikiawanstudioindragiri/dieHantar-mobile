import 'package:flutter/material.dart';

// --- PLACEHOLDER SERVICES ---
// Di aplikasi nyata, ini akan memanggil Firebase Cloud Functions (Python Backend)
// untuk memvalidasi PIN atau mengirim data Rating.
class SecurityService {
  Future<bool> setPin(String pin) async {
    print("Memanggil Python CF: set_pin dengan PIN $pin");
    return true; // Sukses
  }
  Future<bool> authenticateBiometrics() async {
    // Logika otentikasi biometrik menggunakan 'local_auth' Flutter
    await Future.delayed(const Duration(seconds: 1)); 
    return true; 
  }
}

class NotificationService {
  // X. Notification_List
  List<Map<String, dynamic>> getNotifications() => [
    {'id': '1', 'title': 'Pesanan Selesai!', 'body': 'Pesanan #105 telah tiba di tujuan Anda.', 'isRead': false, 'time': '5 menit lalu'},
    {'id': '2', 'title': 'Diskon 50% Menunggumu', 'body': 'Gunakan kode PROMO50 untuk semua makanan.', 'isRead': true, 'time': '1 jam lalu'},
    {'id': '3', 'title': 'Driver Tiba', 'body': 'Driver Budi telah tiba di lokasi penjemputan.', 'isRead': true, 'time': 'Kemarin'},
  ];
  void markAsRead(String id) => print("Notifikasi $id ditandai sebagai sudah dibaca.");
}
// ----------------------------

/// =======================================================================
/// 1. SCREEN PENGATURAN KEAMANAN (F. Set PIN, G. Touch ID)
/// =======================================================================
class SecuritySetupScreen extends StatefulWidget {
  const SecuritySetupScreen({super.key});

  @override
  State<SecuritySetupScreen> createState() => _SecuritySetupScreenState();
}

class _SecuritySetupScreenState extends State<SecuritySetupScreen> {
  final SecurityService _securityService = SecurityService();
  final TextEditingController _pinController = TextEditingController();
  String _message = '';
  bool _isPinSet = false; // Asumsi status PIN dari UserModel (F)
  bool _isTouchIdActive = false; // Status Touch ID (G)

  @override
  void initState() {
    super.initState();
    // Memuat status awal dari service/profil pengguna
    _isPinSet = true; 
    _isTouchIdActive = true;
  }

  void _handlePinSetup() async {
    final pin = _pinController.text;
    if (pin.length != 6) {
      setState(() => _message = "PIN harus 6 digit.");
      return;
    }

    setState(() => _message = "Mengatur PIN...");
    final success = await _securityService.setPin(pin); // Panggil CF Python
    
    if (success) {
      setState(() {
        _isPinSet = true;
        _message = "PIN Keamanan berhasil diatur!";
        _pinController.clear();
      });
    } else {
      setState(() => _message = "Gagal mengatur PIN. Coba lagi.");
    }
  }

  void _handleTouchIdToggle(bool value) async {
    if (value) {
      setState(() => _message = "Mengaktifkan biometrik...");
      final authenticated = await _securityService.authenticateBiometrics();
      if (authenticated) {
        setState(() {
          _isTouchIdActive = true;
          _message = "Autentikasi Biometrik berhasil diaktifkan (G).";
        });
      } else {
        setState(() => _message = "Gagal mengaktifkan biometrik. Pastikan sensor berfungsi.");
      }
    } else {
      setState(() {
        _isTouchIdActive = false;
        _message = "Autentikasi Biometrik dinonaktifkan.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Pengaturan Keamanan'), backgroundColor: Colors.deepOrange),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // --- G. Touch ID Security ---
            SwitchListTile(
              title: const Text('Akses Biometrik (Touch ID/Face ID)'),
              subtitle: const Text('Gunakan sidik jari atau wajah untuk login cepat.'),
              value: _isTouchIdActive,
              onChanged: _isPinSet ? _handleTouchIdToggle : null, // Hanya bisa diaktifkan jika PIN sudah diatur
              secondary: const Icon(Icons.fingerprint, color: Colors.blueGrey),
            ),
            
            const Divider(),

            // --- F. Set PIN Security ---
            Text('PIN Keamanan (F)', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: _isPinSet ? Colors.green : Colors.deepOrange)),
            Text(_isPinSet ? 'PIN Anda sudah diatur.' : 'PIN belum diatur. Harap atur PIN untuk keamanan transaksi.'),
            const SizedBox(height: 10),

            TextField(
              controller: _pinController,
              keyboardType: TextInputType.number,
              maxLength: 6,
              obscureText: true,
              decoration: InputDecoration(
                labelText: _isPinSet ? 'Ubah PIN Baru' : 'Atur PIN Baru (6 digit)',
                border: const OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 10),

            ElevatedButton(
              onPressed: _handlePinSetup,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.deepOrange,
                foregroundColor: Colors.white,
                minimumSize: const Size(double.infinity, 50),
              ),
              child: Text(_isPinSet ? 'Ubah PIN' : 'Atur PIN Sekarang'),
            ),
            const SizedBox(height: 10),

            if (_message.isNotEmpty)
              Text(_message, style: TextStyle(color: _message.contains("berhasil") ? Colors.green : Colors.red)),
          ],
        ),
      ),
    );
  }
}

/// =======================================================================
/// 2. SCREEN PUSAT NOTIFIKASI (X. Notification)
/// =======================================================================
class NotificationScreen extends StatelessWidget {
  final NotificationService _notificationService = NotificationService();
  
  NotificationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final notifications = _notificationService.getNotifications();
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('Pusat Notifikasi (X)'),
        backgroundColor: Colors.blueAccent,
        actions: [
          IconButton(
            icon: const Icon(Icons.mark_email_read),
            onPressed: () => print('Tandai semua sebagai sudah dibaca'),
            tooltip: 'Tandai Semua Sudah Dibaca',
          )
        ],
      ),
      body: ListView.builder(
        itemCount: notifications.length,
        itemBuilder: (context, index) {
          final notif = notifications[index];
          return ListTile(
            leading: Icon(
              notif['isRead'] ? Icons.mail_outline : Icons.mail,
              color: notif['isRead'] ? Colors.grey : Colors.blueAccent,
            ),
            title: Text(notif['title'], style: TextStyle(fontWeight: notif['isRead'] ? FontWeight.normal : FontWeight.bold)),
            subtitle: Text(notif['body'], maxLines: 2, overflow: TextOverflow.ellipsis),
            trailing: Text(notif['time'], style: const TextStyle(fontSize: 12, color: Colors.grey)),
            tileColor: notif['isRead'] ? Colors.white : Colors.blueAccent.withOpacity(0.05),
            onTap: () {
              _notificationService.markAsRead(notif['id']);
              // Navigasi ke detail terkait (misal: Order Tracking Screen)
              print("Membuka detail notifikasi ${notif['id']}");
            },
          );
        },
      ),
    );
  }
}

/// =======================================================================
/// 3. SCREEN RATING & TIPPING (U. Rating)
/// =======================================================================
class FinalOrderReviewScreen extends StatefulWidget {
  final String orderId;
  
  const FinalOrderReviewScreen({super.key, required this.orderId});

  @override
  State<FinalOrderReviewScreen> createState() => _FinalOrderReviewScreenState();
}

class _FinalOrderReviewScreenState extends State<FinalOrderReviewScreen> {
  double _rating = 5.0;
  String _reviewText = '';
  int _tipAmount = 0; // U. Rating_Tipping

  final List<int> _tipOptions = [5000, 10000, 15000];

  void _submitReview() {
    if (_rating < 1.0) {
      print('Rating minimal 1 bintang.');
      return;
    }
    
    // Panggil Cloud Function Python untuk memproses Rating & Tipping
    print('--- Mengirim Review ke CF Python ---');
    print('Order ID: ${widget.orderId}');
    print('Rating: $_rating Bintang');
    print('Review: $_reviewText');
    print('Tip Diberikan: Rp $_tipAmount');

    // Di backend Python (payment_service.py) akan menangani:
    // 1. Menyimpan Rating/Review ke Firestore.
    // 2. Memproses pembayaran tip (menggunakan logika Payment Service).

    Navigator.pop(context); // Kembali ke Home/History
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Review Pesanan Selesai'), backgroundColor: Colors.green),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // U. Rating - Bintang
            const Text('Bagaimana pengalamanmu?', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            const Text('Berikan rating untuk layanan ini.', style: TextStyle(color: Colors.grey)),
            const SizedBox(height: 20),

            Center(
              child: Column(
                children: [
                  Text('$_rating Bintang', style: const TextStyle(fontSize: 36, color: Colors.amber)),
                  const SizedBox(height: 10),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: List.generate(5, (index) {
                      return IconButton(
                        icon: Icon(
                          index < _rating ? Icons.star : Icons.star_border,
                          color: Colors.amber,
                          size: 40,
                        ),
                        onPressed: () {
                          setState(() {
                            _rating = index + 1.0;
                          });
                        },
                      );
                    }),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 30),

            // U. Review - Komentar
            const Text('Tulis Ulasan (Opsional)', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            TextField(
              onChanged: (value) => _reviewText = value,
              maxLines: 4,
              decoration: const InputDecoration(
                hintText: 'Misalnya: Driver sangat ramah dan pengiriman cepat.',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 30),

            // U. Rating_Tipping
            const Text('Berikan Tip untuk Driver', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const Text('Tip sepenuhnya milik Driver.', style: TextStyle(color: Colors.grey)),
            const SizedBox(height: 10),

            Wrap(
              spacing: 10,
              children: [
                ..._tipOptions.map((amount) => ChoiceChip(
                  label: Text('Rp $amount'),
                  selected: _tipAmount == amount,
                  selectedColor: Colors.green.shade100,
                  onSelected: (selected) {
                    setState(() {
                      _tipAmount = selected ? amount : 0;
                    });
                  },
                )),
                ActionChip(
                  label: Text(_tipAmount != 0 && !_tipOptions.contains(_tipAmount) ? 'Rp $_tipAmount (Custom)' : 'Custom'),
                  onPressed: () => print('Buka dialog input tip kustom'),
                  backgroundColor: _tipAmount != 0 && !_tipOptions.contains(_tipAmount) ? Colors.green.shade50 : Colors.grey.shade200,
                )
              ],
            ),
            const SizedBox(height: 40),

            // Tombol Submit
            ElevatedButton(
              onPressed: _submitReview,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green,
                foregroundColor: Colors.white,
                minimumSize: const Size(double.infinity, 50),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
              ),
              child: const Text('Kirim Ulasan & Tip', style: TextStyle(fontSize: 18)),
            ),
          ],
        ),
      ),
    );
  }
}