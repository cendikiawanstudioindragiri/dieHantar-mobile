import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:firebase_auth/firebase_auth.dart';

// Model untuk notifikasi
class NotificationModel {
  final String id;
  final String title;
  final String body;
  final DateTime timestamp;

  NotificationModel({
    required this.id,
    required this.title,
    required this.body,
    required this.timestamp,
  });

  factory NotificationModel.fromJson(Map<String, dynamic> json) {
    return NotificationModel(
      id: json['id'],
      title: json['title'],
      body: json['body'],
      timestamp: DateTime.parse(json['timestamp']),
    );
  }
}

class NotificationScreen extends StatefulWidget {
  const NotificationScreen({super.key});

  @override
  State<NotificationScreen> createState() => _NotificationScreenState();
}

class _NotificationScreenState extends State<NotificationScreen> {
  late Future<List<NotificationModel>> _notificationsFuture;
  final String _baseUrl =
      'YOUR_CLOUD_FUNCTION_BASE_URL'; // TODO: Replace with your actual base URL

  @override
  void initState() {
    super.initState();
    _notificationsFuture = fetchNotifications();
  }

  Future<List<NotificationModel>> fetchNotifications() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) {
      throw Exception('User not authenticated');
    }
    final idToken = await user.getIdToken();
    final url = Uri.parse('$_baseUrl/notificationsAPI');

    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer $idToken'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data['success']) {
        final List<dynamic> notificationData = data['notifications'];
        return notificationData
            .map((json) => NotificationModel.fromJson(json))
            .toList();
      }
    }
    // If something goes wrong, return an empty list or handle error
    return [];
  }

  IconData getIcon(String title) {
    if (title.contains('Order')) return Icons.restaurant_menu;
    if (title.contains('Driver')) return Icons.delivery_dining;
    if (title.contains('Off') || title.contains('Discount')) {
      return Icons.local_offer;
    }
    if (title.contains('Delivered')) return Icons.check_circle;
    return Icons.notifications;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifikasi'),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black87,
        elevation: 1,
      ),
      body: FutureBuilder<List<NotificationModel>>(
        future: _notificationsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return const Center(child: Text('Gagal memuat notifikasi.'));
          }
          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('Tidak ada notifikasi baru.'));
          }

          final notifications = snapshot.data!;
          return ListView.separated(
            itemCount: notifications.length,
            separatorBuilder: (context, index) => const Divider(height: 0),
            itemBuilder: (context, index) {
              final notification = notifications[index];
              return ListTile(
                leading: CircleAvatar(
                  backgroundColor: Colors.teal.withOpacity(0.1),
                  child: Icon(getIcon(notification.title), color: Colors.teal),
                ),
                title: Text(
                  notification.title,
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                subtitle: Text(notification.body),
                trailing: Text(
                  'Now',
                  style: const TextStyle(color: Colors.grey, fontSize: 12),
                ), // Placeholder time
                onTap: () {
                  // Action on tap
                },
              );
            },
          );
        },
      ),
    );
  }
}
