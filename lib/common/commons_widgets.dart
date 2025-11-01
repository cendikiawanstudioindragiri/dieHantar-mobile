import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:myapp/services/firebase_service.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class LocationModel {
  final String id;
  final String name;
  final String address;
  final double lat;
  final double lon;
  final bool isFavorite;

  const LocationModel({
    required this.id,
    required this.name,
    required this.address,
    required this.lat,
    required this.lon,
    this.isFavorite = false,
  });

  // Add fromFirestore and toMap methods
  factory LocationModel.fromFirestore(DocumentSnapshot doc) {
    Map data = doc.data() as Map<String, dynamic>; // Cast to be safe
    return LocationModel(
      id: doc.id,
      name: data['name'] ?? '',
      address: data['address'] ?? '',
      lat: (data['lat'] ?? 0.0).toDouble(), // Ensure double
      lon: (data['lon'] ?? 0.0).toDouble(), // Ensure double
      isFavorite: data['isFavorite'] ?? false,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'name': name,
      'address': address,
      'lat': lat,
      'lon': lon,
      'isFavorite': isFavorite,
    };
  }
}

class ProductModel {
  final String id;
  final String name;
  final double price;

  const ProductModel({
    required this.id,
    required this.name,
    required this.price,
  });
}

/// =======================================================================
/// 1. I. SELECT LOCATION (My location, My Location_Add New Location)
/// =======================================================================
class LocationSelectionScreen extends StatelessWidget {
  final DataService _dataService = DataService();

  LocationSelectionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Pilih Lokasi Pengiriman'),
        backgroundColor: Colors.teal,
      ),
      body: StreamBuilder<QuerySnapshot>(
        stream: _dataService.userLocationsStream(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError ||
              !snapshot.hasData ||
              snapshot.data!.docs.isEmpty) {
            return const Center(child: Text("Belum ada lokasi tersimpan."));
          }

          final locations = snapshot.data!.docs
              .map((doc) => LocationModel.fromFirestore(doc))
              .toList();
          final favoriteLocations = locations
              .where((l) => l.isFavorite)
              .toList();
          final otherLocations = locations.where((l) => !l.isFavorite).toList();

          return SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildCurrentLocation(),
                if (favoriteLocations.isNotEmpty)
                  _buildLocationList(
                    'Lokasi Favorit',
                    favoriteLocations,
                    Icons.favorite,
                    context,
                  ),
                _buildLocationList(
                  'Lokasi Lainnya',
                  otherLocations,
                  Icons.place,
                  context,
                ),
                const Divider(),
                ListTile(
                  leading: const Icon(
                    Icons.add_location_alt,
                    color: Colors.teal,
                  ),
                  title: const Text(
                    'Tambah Lokasi Baru',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  onTap: () {
                    _showAddLocationForm(context);
                  },
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildCurrentLocation() {
    return Container(
      padding: const EdgeInsets.all(16),
      color: Colors.teal.withAlpha(25), // Replaced withOpacity
      child: const Row(
        children: [
          Icon(Icons.gps_fixed, color: Colors.teal),
          SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Lokasi Saya Saat Ini',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                Text(
                  'Gunakan GPS Anda',
                  style: TextStyle(fontSize: 12, color: Colors.grey),
                ),
              ],
            ),
          ),
          Icon(Icons.arrow_forward_ios, size: 16),
        ],
      ),
    );
  }

  Widget _buildLocationList(
    String title,
    List<LocationModel> locations,
    IconData icon,
    BuildContext context,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text(
            title,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
        ),
        ...locations.map(
          (loc) => ListTile(
            leading: Icon(icon, color: Colors.blueGrey),
            title: Text(loc.name),
            subtitle: Text(
              loc.address,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            trailing: loc.isFavorite
                ? const Icon(Icons.star, color: Colors.amber)
                : null,
            onTap: () {
              // Handle location selection
              Navigator.pop(context, loc); // Example action
            },
          ),
        ),
      ],
    );
  }

  void _showAddLocationForm(BuildContext context) {
    final nameController = TextEditingController();
    final addressController = TextEditingController();

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (context) {
        return Padding(
          padding: EdgeInsets.only(
            bottom: MediaQuery.of(context).viewInsets.bottom,
            left: 16,
            right: 16,
            top: 16,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                'Tambah Alamat Baru',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 15),
              TextField(
                controller: nameController,
                decoration: InputDecoration(
                  labelText: 'Nama Lokasi (cth: Rumah, Kantor)',
                ),
              ),
              const SizedBox(height: 10),
              TextField(
                controller: addressController,
                decoration: InputDecoration(labelText: 'Alamat Lengkap'),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  final newLocation = LocationModel(
                    id: '', // Firestore will generate this
                    name: nameController.text,
                    address: addressController.text,
                    lat: 0, // Placeholder, ideally get from a map picker
                    lon: 0, // Placeholder
                  );
                  _dataService.addUserLocation(newLocation.toMap());
                  Navigator.pop(context);
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.teal,
                  minimumSize: const Size(double.infinity, 50),
                ),
                child: const Text(
                  'Simpan Alamat',
                  style: TextStyle(color: Colors.white),
                ),
              ),
              const SizedBox(height: 10),
            ],
          ),
        );
      },
    );
  }
}

// ... (rest of the file remains the same for now)


/// =======================================================================
/// 2. L/M/N. DETAIL PRODUK, ULASAN & SHARE (Foods, Drinks, Service)
/// =======================================================================
class ProductDetailScreen extends StatefulWidget {
  final ProductModel product;
  const ProductDetailScreen({super.key, required this.product});

  @override
  State<ProductDetailScreen> createState() => _ProductDetailScreenState();
}

class _ProductDetailScreenState extends State<ProductDetailScreen> {
  int quantity = 1;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 250,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              title: Text(
                widget.product.name,
                style: const TextStyle(shadows: [Shadow(blurRadius: 5)]),
              ),
              background: Container(
                color: Colors.grey[200],
              ), // L. Foods_Detail (Gambar Produk)
            ),
            actions: [
              // L. Foods_Detail_Share freinds
              IconButton(
                icon: const Icon(Icons.share),
                onPressed: () { /* Handle share */ },
              ),
            ],
          ),
          SliverList(
            delegate: SliverChildListDelegate([
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Rp ${widget.product.price}',
                      style: const TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.redAccent,
                      ),
                    ),
                    const SizedBox(height: 10),

                    // Deskripsi (L. Foods_Detail_See more)
                    const Text("product description"),
                    TextButton(
                      onPressed: () { /* Handle see more */ },
                      child: const Text(
                        'Lihat Selengkapnya',
                        style: TextStyle(color: Colors.teal),
                      ),
                    ),
                    const Divider(),

                    // Ulasan & Rating (L. Foods_Detail_See All Review)
                    _buildReviewSummary(context),
                    const Divider(),

                    // Opsi Pilihan (L. Foods_Detail_select 2)
                    _buildProductOptions(),
                  ],
                ),
              ),
            ]),
          ),
        ],
      ),
      bottomNavigationBar: _buildBottomBar(context),
    );
  }

  Widget _buildReviewSummary(BuildContext context) {
    // L. Foods_Detail_See All Review, L. Foods_Detail_See all review
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                const Icon(Icons.star, color: Colors.amber, size: 20),
                const SizedBox(width: 5),
                Text(
                  '4.5 (120 ulasan)',
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              ],
            ),
            TextButton(
              onPressed: () { /* Navigate to all reviews */ },
              child: const Text(
                'Lihat Semua Ulasan',
                style: TextStyle(color: Colors.teal),
              ),
            ),
          ],
        ),
        // Simulasi 1 ulasan terbaru
        const SizedBox(height: 8),
        const Text(
          '“Rasanya enak, pengiriman cepat!”',
          style: TextStyle(fontStyle: FontStyle.italic, color: Colors.grey),
        ),
        const Text(
          '- Oleh User A',
          style: TextStyle(fontSize: 12, color: Colors.grey),
        ),
      ],
    );
  }

  Widget _buildProductOptions() {
    // L. Foods_Detail_select
    return const Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Pilihan Rasa',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        Wrap(
          spacing: 8.0,
          children: [
            Chip(label: Text('Original'), backgroundColor: Colors.teal),
            Chip(label: Text('Pedas')),
            Chip(label: Text('Keju')),
          ],
        ),
      ],
    );
  }

  Widget _buildBottomBar(BuildContext context) {
    // L. Foods_Add Basket
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 10)],
      ),
      child: Row(
        children: [
          // Kontrol Kuantitas
          Row(
            children: [
              IconButton(
                icon: const Icon(
                  Icons.remove_circle_outline,
                  color: Colors.teal,
                ),
                onPressed: () {
                  setState(() {
                    if (quantity > 1) quantity--;
                  });
                },
              ),
              Text(
                '$quantity',
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              IconButton(
                icon: const Icon(Icons.add_circle_outline, color: Colors.teal),
                onPressed: () {
                  setState(() {
                    quantity++;
                  });
                },
              ),
            ],
          ),
          const SizedBox(width: 15),
          // Tombol Tambah ke Keranjang
          Expanded(
            child: ElevatedButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(
                      '${widget.product.name} berhasil ditambahkan!',
                    ),
                  ),
                );
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.teal,
                padding: const EdgeInsets.symmetric(vertical: 12),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
              child: Text(
                'Tambah ke Keranjang (Rp ${widget.product.price * quantity})',
                style: const TextStyle(color: Colors.white, fontSize: 16),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

/// =======================================================================
/// 3. R. DRIVER CONTACT (message, message-attachment, call)
/// =======================================================================
class ChatScreen extends StatefulWidget {
  final String driverId;
  const ChatScreen({super.key, required this.driverId});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  final List<Map<String, dynamic>> _messages = [
    {
      'text': 'Halo, saya sudah sampai di depan restoran.',
      'isMe': false,
      'time': '10:05',
    },
    {'text': 'Oke, saya tunggu di lobi.', 'isMe': true, 'time': '10:06'},
    // R. message 2
  ];

  void _sendMessage() {
    if (_messageController.text.trim().isNotEmpty) {
      setState(() {
        _messages.add({
          'text': _messageController.text.trim(),
          'isMe': true,
          'time': DateTime.now().toString().substring(11, 16),
        });
      });
      // Logika Firestore: Kirim pesan ke subkoleksi 'driver_chats'
      _messageController.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Driver Budi'),
        backgroundColor: Colors.teal,
        actions: [
          // R. call
          IconButton(
            icon: const Icon(Icons.call),
            onPressed: () { /* Handle call */ },
          ),
          // R. report account &bug
          IconButton(
            icon: const Icon(Icons.more_vert),
            onPressed: () { /* Handle report */ },
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            // Daftar pesan (real-time stream dari Firestore)
            child: ListView.builder(
              reverse: true,
              padding: const EdgeInsets.all(8.0),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[_messages.length - 1 - index];
                return _buildChatMessage(message);
              },
            ),
          ),
          // Input pesan
          _buildChatInput(),
        ],
      ),
    );
  }

  Widget _buildChatMessage(Map<String, dynamic> message) {
    final bool isMe = message['isMe'] as bool;
    return Align(
      alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
        padding: const EdgeInsets.all(12),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.7,
        ),
        decoration: BoxDecoration(
          color: isMe ? Colors.teal : Colors.grey[300],
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: isMe ? const Radius.circular(16) : Radius.zero,
            bottomRight: isMe ? Radius.zero : const Radius.circular(16),
          ),
        ),
        child: Column(
          crossAxisAlignment: isMe
              ? CrossAxisAlignment.end
              : CrossAxisAlignment.start,
          children: [
            Text(
              message['text'] as String,
              style: TextStyle(color: isMe ? Colors.white : Colors.black87),
            ),
            const SizedBox(height: 4),
            Text(
              message['time'] as String,
              style: TextStyle(
                fontSize: 10,
                color: isMe ? Colors.white70 : Colors.black54,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildChatInput() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      color: Colors.white,
      child: Row(
        children: [
          // R. message-attachment
          IconButton(
            icon: const Icon(Icons.attach_file, color: Colors.teal),
            onPressed: () { /* Handle attachment */ },
          ),
          Expanded(
            child: TextField(
              controller: _messageController,
              decoration: InputDecoration(
                hintText: 'Ketik pesan Anda...',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(20),
                  borderSide: BorderSide.none,
                ),
                filled: true,
                fillColor: Colors.grey[200],
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 8,
                ),
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.send, color: Colors.teal),
            onPressed: _sendMessage,
          ),
        ],
      ),
    );
  }
}

/// =======================================================================
/// 4. X. NOTIFICATION (Notification, search)
/// =======================================================================
class NotificationScreen extends StatefulWidget {
  const NotificationScreen({super.key});

  @override
  State<NotificationScreen> createState() => _NotificationScreenState();
}

class _NotificationScreenState extends State<NotificationScreen> {
  String _searchQuery = '';

  final List<Map<String, dynamic>> _allNotifications = [
    {
      'title': 'Pesanan Selesai!',
      'body': 'Pesanan #12345 telah berhasil diantar.',
      'type': 'order',
      'read': false,
    },
    {
      'title': 'Promo Terbaru',
      'body': 'Diskon 20% untuk semua makanan hari ini!',
      'type': 'promo',
      'read': true,
    },
    {
      'title': 'Peringatan',
      'body': 'Akses lokasi Anda dimatikan.',
      'type': 'info',
      'read': false,
    },
    {
      'title': 'Driver Tiba',
      'body': 'Driver Anda sudah tiba di lokasi penjemputan.',
      'type': 'order',
      'read': true,
    },
  ];

  @override
  Widget build(BuildContext context) {
    final filteredNotifications = _allNotifications.where((n) {
      if (_searchQuery.isEmpty) {
        return true;
      }
      // X. notification_search
      final title = n['title'] as String? ?? '';
      final body = n['body'] as String? ?? '';
      return title.toLowerCase().contains(_searchQuery.toLowerCase()) ||
          body.toLowerCase().contains(_searchQuery.toLowerCase());
    }).toList();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifikasi'),
        backgroundColor: Colors.teal,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: TextField(
              decoration: InputDecoration(
                hintText: 'Cari notifikasi...',
                prefixIcon: const Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                  borderSide: BorderSide.none,
                ),
                filled: true,
                fillColor: Colors.grey[200],
              ),
              onChanged: (value) {
                setState(() {
                  _searchQuery = value;
                });
              },
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: filteredNotifications.length,
              itemBuilder: (context, index) {
                final notification = filteredNotifications[index];
                final isRead = notification['read'] as bool? ?? false;
                final type = notification['type'] as String? ?? 'info';

                return ListTile(
                  leading: CircleAvatar(
                    backgroundColor: isRead
                        ? Colors.grey[400]
                        : Colors.teal,
                    child: Icon(
                      type == 'order'
                          ? Icons.receipt_long
                          : type == 'promo'
                          ? Icons.campaign
                          : Icons.info,
                      color: Colors.white,
                    ),
                  ),
                  title: Text(
                    notification['title'] as String? ?? '',
                    style: TextStyle(
                      fontWeight: isRead
                          ? FontWeight.normal
                          : FontWeight.bold,
                    ),
                  ),
                  subtitle: Text(notification['body'] as String? ?? ''),
                  trailing: !isRead
                      ? Container(
                          width: 10,
                          height: 10,
                          decoration: const BoxDecoration(
                            color: Colors.red,
                            shape: BoxShape.circle,
                          ),
                        )
                      : null,
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
