import 'package:flutter/material.dart';
import 'package:myapp/food/models/restaurant_model.dart';
import 'package:myapp/food/models/category_model.dart';
import 'package:myapp/food/models/promotion_model.dart';
import 'package:myapp/food/models/menu_item_model.dart';

class FoodService {
  // Mengambil daftar promosi
  Future<List<Promotion>> getPromotions() async {
    // Simulasi panggilan jaringan
    await Future.delayed(const Duration(seconds: 1));

    return [
      Promotion(
        id: '1',
        title: 'Diskon 50% Untukmu!',
        imageUrl:
            'https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=2070&auto=format&fit=crop',
      ),
      Promotion(
        id: '2',
        title: 'Gratis Ongkir Sepuasnya!',
        imageUrl:
            'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=1981&auto=format&fit=crop',
      ),
      Promotion(
        id: '3',
        title: 'Menu Baru, Wajib Coba!',
        imageUrl:
            'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?q=80&w=1887&auto=format&fit=crop',
      ),
    ];
  }

  // Mengambil daftar kategori
  Future<List<FoodCategory>> getCategories() async {
    await Future.delayed(const Duration(milliseconds: 500));
    return [
      FoodCategory(id: '1', name: 'Nasi', icon: Icons.rice_bowl),
      FoodCategory(id: '2', name: 'Cepat Saji', icon: Icons.fastfood),
      FoodCategory(id: '3', name: 'Minuman', icon: Icons.local_drink),
      FoodCategory(id: '4', name: 'Jajanan', icon: Icons.cake),
      FoodCategory(id: '5', name: 'Mie', icon: Icons.ramen_dining),
      FoodCategory(id: '6', name: 'Sehat', icon: Icons.health_and_safety),
    ];
  }

  // Mengambil daftar restoran terdekat
  Future<List<Restaurant>> getNearbyRestaurants() async {
    await Future.delayed(const Duration(seconds: 2));
    return [
      Restaurant(
        id: '1',
        name: 'Sate Ayam Pak Budi',
        cuisine: 'Sate, Indonesia',
        rating: 4.5,
        distance: '1.2 km',
        imageUrl:
            'https://images.unsplash.com/photo-1604382354936-07c5d9983d34?q=80&w=2070&auto=format&fit=crop',
      ),
      Restaurant(
        id: '2',
        name: 'Bakso Malang Cak Man',
        cuisine: 'Bakso, Jajanan',
        rating: 4.8,
        distance: '0.8 km',
        imageUrl:
            'https://images.unsplash.com/photo-1572656631137-7935297eff55?q=80&w=1887&auto=format&fit=crop',
      ),
      Restaurant(
        id: '3',
        name: 'Gudeg Yu Djum',
        cuisine: 'Gudeg, Jawa',
        rating: 4.7,
        distance: '2.5 km',
        imageUrl:
            'https://images.unsplash.com/photo-1559847844-5315695d0464?q=80&w=2070&auto=format&fit=crop',
      ),
      Restaurant(
        id: '4',
        name: 'Pizza Ria',
        cuisine: 'Pizza, Italia',
        rating: 4.6,
        distance: '3.1 km',
        imageUrl:
            'https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=2070&auto=format&fit=crop',
      ),
    ];
  }

  // Mengambil menu untuk restoran tertentu
  Future<List<MenuItem>> getMenuItems(String restaurantId) async {
    await Future.delayed(const Duration(seconds: 1));

    // Data tiruan - dalam aplikasi nyata, ini akan bergantung pada restaurantId
    return [
      MenuItem(
        id: 'm1',
        name: 'Sate Ayam (10 tusuk)',
        description: 'Sate ayam dengan bumbu kacang spesial.',
        price: 25000,
        imageUrl:
            'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?q=80&w=1887&auto=format&fit=crop',
      ),
      MenuItem(
        id: 'm2',
        name: 'Nasi Goreng Spesial',
        description: 'Nasi goreng dengan telur, ayam, dan udang.',
        price: 30000,
        imageUrl:
            'https://images.unsplash.com/photo-1512058564366-18510be2db19?q=80&w=2072&auto=format&fit=crop',
      ),
      MenuItem(
        id: 'm3',
        name: 'Es Teh Manis',
        description: 'Teh manis dingin yang menyegarkan.',
        price: 5000,
        imageUrl:
            'https://images.unsplash.com/photo-1579584736814-159d4c389a07?q=80&w=1887&auto=format&fit=crop',
      ),
      MenuItem(
        id: 'm4',
        name: 'Gado-Gado',
        description: 'Salad sayuran dengan saus kacang.',
        price: 20000,
        imageUrl:
            'https://images.unsplash.com/photo-1623855101524-39a58933a253?q=80&w=1887&auto=format&fit=crop',
      ),
    ];
  }
}
