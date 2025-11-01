import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import 'package:myapp/providers/cart_provider.dart';

class RestaurantDetailScreen extends StatelessWidget {
  final String restaurantName;

  const RestaurantDetailScreen({super.key, required this.restaurantName});

  @override
  Widget build(BuildContext context) {
    final cart = Provider.of<CartProvider>(context, listen: false);

    // Data menu dummy berdasarkan nama restoran
    final Map<String, List<Map<String, dynamic>>> dummyMenus = {
      'Sate Ayam Madura': [
        {
          'name': 'Sate Ayam (10 tusuk)',
          'price': 25000,
          'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1',
        },
        {
          'name': 'Lontong',
          'price': 5000,
          'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1',
        },
      ],
      'Pizza Place': [
        {
          'name': 'Pepperoni Pizza',
          'price': 85000,
          'image':
              'https://images.unsplash.com/photo-1513104890138-7c749659a591',
        },
        {
          'name': 'Margherita Pizza',
          'price': 75000,
          'image':
              'https://images.unsplash.com/photo-1513104890138-7c749659a591',
        },
      ],
      'Coffee Corner': [
        {
          'name': 'Espresso',
          'price': 20000,
          'image':
              'https://images.unsplash.com/photo-1497935586351-b67a49e012bf',
        },
        {
          'name': 'Cappuccino',
          'price': 28000,
          'image':
              'https://images.unsplash.com/photo-1497935586351-b67a49e012bf',
        },
      ],
    };

    final menu = dummyMenus[restaurantName] ?? [];

    return Scaffold(
      appBar: AppBar(
        title: Text(restaurantName),
        actions: [
          TextButton.icon(
            onPressed: () {
              context.go('/reviews', extra: restaurantName);
            },
            icon: const Icon(Icons.reviews, color: Colors.white),
            label: const Text('Ulasan', style: TextStyle(color: Colors.white)),
          ),
          Consumer<CartProvider>(
            builder: (_, cart, ch) =>
                Badge(label: Text(cart.itemCount.toString()), child: ch),
            child: IconButton(
              icon: const Icon(Icons.shopping_cart),
              onPressed: () {
                context.go('/cart');
              },
            ),
          ),
        ],
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
              title: Text(
                item['name'],
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              subtitle: Text('Rp ${item['price']}'),
              trailing: IconButton(
                icon: const Icon(Icons.add_shopping_cart, color: Colors.teal),
                onPressed: () {
                  cart.addItem(item['name'], item['price']);
                  ScaffoldMessenger.of(context).hideCurrentSnackBar();
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                        '${item['name']} ditambahkan ke keranjang!',
                      ),
                      duration: const Duration(seconds: 2),
                      action: SnackBarAction(
                        label: 'UNDO',
                        onPressed: () {
                          cart.removeSingleItem(item['name']);
                        },
                      ),
                    ),
                  );
                },
              ),
            ),
          );
        },
      ),
    );
  }
}
