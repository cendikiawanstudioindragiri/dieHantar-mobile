import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import 'package:myapp/providers/cart_provider.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _searchController = TextEditingController();

  void _navigateToRestaurantDetail(String restaurantName) {
    context.go('/restaurant-detail', extra: restaurantName);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Beranda'),
        actions: [
          Consumer<CartProvider>(
            builder: (_, cart, ch) => Badge(
              label: Text(cart.itemCount.toString()),
              child: ch,
            ),
            child: IconButton(
              icon: const Icon(Icons.shopping_cart),
              onPressed: () {
                context.go('/cart');
              },
            ),
          ),
          IconButton(
            icon: const Icon(Icons.notifications_none),
            onPressed: () => context.go('/notifications'),
          ),
        ],
      ),
      body: ListView(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Mau makan apa hari ini?',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 20),
                _buildSearchField(),
                const SizedBox(height: 30),
                _buildSectionTitle('Kategori'),
                _buildCategoryList(),
                const SizedBox(height: 30),
                _buildSectionTitle('Restoran Terdekat'),
              ],
            ),
          ),
          _buildRestaurantList(),
        ],
      ),
    );
  }

  Widget _buildSearchField() {
    return TextField(
      controller: _searchController,
      decoration: InputDecoration(
        hintText: 'Cari makanan atau restoran...',
        prefixIcon: const Icon(Icons.search),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
        ),
        filled: true,
        fillColor: Colors.grey[200],
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Text(
      title,
      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
    );
  }

  Widget _buildCategoryList() {
    // Data kategori dummy
    final categories = [
      {'name': 'Asia', 'icon': Icons.ramen_dining},
      {'name': 'Barat', 'icon': Icons.fastfood},
      {'name': 'Minuman', 'icon': Icons.local_bar},
      {'name': 'Manis', 'icon': Icons.cake},
    ];

    return SizedBox(
      height: 100,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: categories.length,
        itemBuilder: (context, index) {
          return _buildCategoryItem(
            categories[index]['name'] as String,
            categories[index]['icon'] as IconData,
          );
        },
      ),
    );
  }

  Widget _buildCategoryItem(String name, IconData icon) {
    return Container(
      width: 80,
      margin: const EdgeInsets.only(right: 15, top: 15),
      child: Column(
        children: [
          CircleAvatar(
            radius: 30,
            backgroundColor: Colors.teal.withOpacity(0.1),
            child: Icon(icon, color: Colors.teal, size: 30),
          ),
          const SizedBox(height: 5),
          Text(name, style: const TextStyle(fontSize: 12)),
        ],
      ),
    );
  }

  Widget _buildRestaurantList() {
    // Data restoran dummy
    final restaurants = [
      {
        'name': 'Sate Ayam Madura',
        'image': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4',
        'rating': 4.5,
      },
      {
        'name': 'Pizza Place',
        'image': 'https://images.unsplash.com/photo-1513104890138-7c749659a591',
        'rating': 4.8,
      },
      {
        'name': 'Coffee Corner',
        'image': 'https://images.unsplash.com/photo-1497935586351-b67a49e012bf',
        'rating': 4.6,
      },
    ];

    return SizedBox(
      height: 220,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.only(left: 16),
        itemCount: restaurants.length,
        itemBuilder: (context, index) {
          final restaurant = restaurants[index];
          return GestureDetector(
            onTap: () => _navigateToRestaurantDetail(restaurant['name'] as String),
            child: _buildRestaurantCard(
              restaurant['name'] as String,
              restaurant['image'] as String,
              restaurant['rating'] as double,
            ),
          );
        },
      ),
    );
  }

  Widget _buildRestaurantCard(String name, String imageUrl, double rating) {
    return Container(
      width: 250,
      margin: const EdgeInsets.only(right: 15, bottom: 15),
      child: Card(
        clipBehavior: Clip.antiAlias,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
        elevation: 3,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(
              height: 120,
              width: double.infinity,
              child: Image.network(imageUrl, fit: BoxFit.cover),
            ),
            Padding(
              padding: const EdgeInsets.all(12.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(name, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 5),
                  Row(
                    children: [
                      const Icon(Icons.star, color: Colors.amber, size: 18),
                      const SizedBox(width: 4),
                      Text(rating.toString(), style: const TextStyle(fontWeight: FontWeight.bold)),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
}
