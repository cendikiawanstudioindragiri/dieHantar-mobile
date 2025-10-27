
import 'package:flutter/material.dart';

class NotificationScreen extends StatelessWidget {
  const NotificationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Di aplikasi nyata, data ini akan datang dari backend atau stream
    final List<Map<String, String>> notifications = [
      {
        'title': 'Pesanan Diproses',
        'subtitle': 'Pesanan #12345 Anda sedang disiapkan oleh restoran.',
        'time': 'Baru saja',
        'icon': 'processing',
      },
      {
        'title': 'Driver Ditemukan',
        'subtitle': 'Budi Santoso sedang dalam perjalanan untuk mengambil pesanan Anda.',
        'time': '2 menit yang lalu',
        'icon': 'driver',
      },
      {
        'title': 'Diskon Spesial Untuk Anda!',
        'subtitle': 'Dapatkan diskon 50% untuk pesanan berikutnya. Jangan sampai ketinggalan!',
        'time': '1 jam yang lalu',
        'icon': 'promo',
      },
      {
        'title': 'Pesanan Selesai',
        'subtitle': 'Pesanan #12344 telah berhasil dikirim. Beri ulasan Anda!',
        'time': '3 jam yang lalu',
        'icon': 'delivered',
      },
    ];

    IconData getIcon(String icon) {
      switch (icon) {
        case 'processing':
          return Icons.restaurant_menu;
        case 'driver':
          return Icons.delivery_dining;
        case 'promo':
          return Icons.local_offer;
        case 'delivered':
          return Icons.check_circle;
        default:
          return Icons.notifications;
      }
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifikasi'),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black87,
        elevation: 1,
      ),
      body: ListView.separated(
        itemCount: notifications.length,
        separatorBuilder: (context, index) => const Divider(height: 0),
        itemBuilder: (context, index) {
          final notification = notifications[index];
          return ListTile(
            leading: CircleAvatar(
              backgroundColor: Colors.teal.withOpacity(0.1),
              child: Icon(getIcon(notification['icon']!), color: Colors.teal),
            ),
            title: Text(notification['title']!, style: const TextStyle(fontWeight: FontWeight.bold)),
            subtitle: Text(notification['subtitle']!),
            trailing: Text(notification['time']!, style: const TextStyle(color: Colors.grey, fontSize: 12)),
            onTap: () {
              // Aksi saat notifikasi di-tap
            },
          );
        },
      ),
    );
  }
}
