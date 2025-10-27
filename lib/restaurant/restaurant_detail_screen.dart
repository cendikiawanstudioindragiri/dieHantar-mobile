import 'package:flutter/material.dart';

class RestaurantDetailScreen extends StatelessWidget {
  final String restaurantName;

  const RestaurantDetailScreen({super.key, required this.restaurantName});

  @override
  Widget build(BuildContext context) {
    // Data menu dummy berdasarkan nama restoran
    final Map<String, List<Map<String, dynamic>>> dummyMenus = {
      'Sate Ayam Madura': [
        {'name': 'Sate Ayam (10 tusuk)', 'price': 25000, 'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1'},
        {'name': 'Lontong', 'price': 5000, 'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1'},
      ],
      'Pizza Place': [
        {'name': 'Pepperoni Pizza', 'price': 85000, 'image': 'https://images.unsplash.com/photo-1513104890138-7c749659a591'},
        {'name': 'Margherita Pizza', 'price': 75000, 'image': 'https://images.unsplash.com/photo-1513104890138-7c749659a591'},
      ],
      'Coffee Corner': [
        {'name': 'Espresso', 'price': 20000, 'image': 'https://images.unsplash.com/photo-1497935586351-b67a49e012bf'},
        {'name': 'Cappuccino', 'price': 28000, 'image': 'https://images.unsplash.com/photo-1497935586351-b67a49e012bf'},
      ],
    };

    final menu = dummyMenus[restaurantName] ?? [];

    return Scaffold(
      appBar: AppBar(
        title: Text(restaurantName),
      ),
      body: ListView.builder(
        itemCount: menu.length,
        itemBuilder: (context, index) {
          final item = menu[index];
          return Card(
            margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: ListTile(
              leading: Image.network(
                item['image'],
                width: 70,
                height: 70,
                fit: BoxFit.cover,
              ),
              title: Text(item['name'], style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('Rp ${item['price']}'),
              trailing: IconButton(
                icon: const Icon(Icons.add_shopping_cart, color: Colors.teal),
                onPressed: () {
                  // Tambahkan ke keranjang
                },
              ),
            ),
          );
        },
      ),
    );
  }
}
