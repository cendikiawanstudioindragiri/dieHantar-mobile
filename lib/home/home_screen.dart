import 'package:flutter/material.dart';
import 'package:myapp/services/firebase_service.dart';

// --- PLACEHOLDER MODELS & SERVICES ---
class PromoModel { final String title; final String subtitle; final Color color; PromoModel({this.title = 'Diskon 50%', this.subtitle = 'Min. Pembelian Rp 30K', this.color = Colors.red}); }
class ServiceModel { final String title; final IconData icon; final Color color; ServiceModel({required this.title, required this.icon, this.color = Colors.teal}); }

class DataService {
  Future<List<PromoModel>> getActivePromotions() async => [
    PromoModel(title: 'Diskon 50% Semua Makanan!', subtitle: 'Khusus pengguna baru.', color: Colors.deepOrange),
    PromoModel(title: 'Cashback 20% Pay', subtitle: 'Bayar pakai dieHantar Pay.', color: Colors.blue),
  ];
  
  // K, L, M, N. Daftar layanan utama
  List<ServiceModel> getCoreServices() => [
    ServiceModel(title: 'Food', icon: Icons.restaurant, color: Colors.redAccent),
    ServiceModel(title: 'Ride', icon: Icons.directions_bike, color: Colors.green),
    ServiceModel(title: 'Send', icon: Icons.local_shipping, color: Colors.purple),
    ServiceModel(title: 'Mart', icon: Icons.shopping_basket, color: Colors.orange),
    ServiceModel(title: 'Bills', icon: Icons.receipt_long, color: Colors.blue),
    ServiceModel(title: 'Health', icon: Icons.health_and_safety, color: Colors.pink),
  ];
  
  // Data untuk Pencarian Universal
  List<String> getProductList() => ['Nasi Goreng', 'Kopi Susu', 'Servis Motor', 'Burger Jumbo'];
  List<String> getHelpTopics() => ['Cara Reset PIN', 'Masalah Driver', 'Laporkan Pesanan Hilang'];
}
// ------------------------------------

class LocationModel {
  final String id;
  final String name;
  final String address;
  final double lat;
  final double lon;

  const LocationModel({
    required this.id,
    required this.name,
    required this.address,
    required this.lat,
    required this.lon,
  });
}

/// =======================================================================
/// 1. HOME SCREEN (DASHBOARD UTAMA) (H, J, K, L, M, N)
/// =======================================================================
class HomeScreen extends StatelessWidget {
  final UserModel currentUser = UserModel(uid: '', phoneNumber: '');
  final LocationModel currentAddress = const LocationModel(id: '', name: "Rumah", address: "Jl. Sudirman 123", lat: 0, lon: 0);
  final DataService _dataService = DataService();

  HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      body: CustomScrollView(
        slivers: [
          _buildSliverAppBar(context),
          
          SliverList(
            delegate: SliverChildListDelegate(
              [
                _buildWalletCard(context), // Integrasi S
                _buildServiceGrid(context), // K, L, M, N
                _buildPromoSection(), // J. Promo
                _buildDiscoverySection('Rekomendasi Makanan Dekat Anda'),
                _buildDiscoverySection('Layanan Populer'),
                const SizedBox(height: 50),
              ],
            ),
          ),
        ],
      ),
    );
  }

  SliverAppBar _buildSliverAppBar(BuildContext context) {
    return SliverAppBar(
      pinned: true,
      floating: true,
      expandedHeight: 120,
      backgroundColor: Colors.white,
      foregroundColor: Colors.black87,
      flexibleSpace: FlexibleSpaceBar(
        titlePadding: EdgeInsets.zero,
        centerTitle: false,
        title: _buildLocationAndGreeting(context),
      ),
      actions: [
        // X. Notification (Ikon Notifikasi)
        IconButton(
          icon: const Icon(Icons.notifications_none, color: Colors.black87), 
          onPressed: () => print('Navigasi ke Notification Screen (X)'),
        ),
      ],
      bottom: PreferredSize(
        preferredSize: const Size.fromHeight(50),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
          // Z. Search (Bar Pencarian)
          child: _buildSearchBox(context),
        ),
      ),
    );
  }

  Widget _buildLocationAndGreeting(BuildContext context) {
    // H. Home Screen
    return Padding(
      padding: const EdgeInsets.only(left: 16.0, bottom: 8.0),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Halo, ${currentUser.fullName.split(' ').first}!', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          InkWell(
            onTap: () => print('Navigasi ke Location Selection (I)'),
            child: Row(
              children: [
                const Icon(Icons.location_on, size: 16, color: Colors.redAccent),
                const SizedBox(width: 4),
                // I. My locations
                Expanded(child: Text(currentAddress.address, style: const TextStyle(fontSize: 12, color: Colors.grey), overflow: TextOverflow.ellipsis)),
                const Icon(Icons.keyboard_arrow_down, size: 16, color: Colors.grey),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSearchBox(BuildContext context) {
    // Z. Universal Search
    return GestureDetector(
      onTap: () {
        Navigator.push(context, MaterialPageRoute(builder: (_) => SearchScreen()));
      },
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        decoration: BoxDecoration(
          color: Colors.grey[200],
          borderRadius: BorderRadius.circular(25),
        ),
        child: const Row(
          children: [
            Icon(Icons.search, color: Colors.grey),
            SizedBox(width: 10),
            Text('Cari makanan, ojek, atau layanan...', style: TextStyle(color: Colors.grey)),
          ],
        ),
      ),
    );
  }

  Widget _buildWalletCard(BuildContext context) {
    // S. Payment Methods (Quick view)
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(15),
        boxShadow: [BoxShadow(color: Colors.grey.shade200, blurRadius: 8, offset: const Offset(0, 4))],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              const Icon(Icons.account_balance_wallet, color: Colors.teal, size: 30),
              const SizedBox(width: 10),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('dieHantar Pay', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  Text('Rp 150000', style: const TextStyle(color: Colors.teal, fontWeight: FontWeight.bold)),
                ],
              ),
            ],
          ),
          ElevatedButton.icon(
            onPressed: () => print('Navigasi ke Top Up Screen (S)'),
            icon: const Icon(Icons.add_circle_outline, size: 18),
            label: const Text('Top Up'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.teal,
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
            ),
          )
        ],
      ),
    );
  }

  Widget _buildServiceGrid(BuildContext context) {
    // K, L, M, N (Katalog Layanan Utama)
    final services = _dataService.getCoreServices();
    return Padding(
      padding: const EdgeInsets.only(left: 16.0, right: 16.0, bottom: 20.0),
      child: GridView.builder(
        physics: const NeverScrollableScrollPhysics(), // Menonaktifkan scroll di dalam grid
        shrinkWrap: true,
        itemCount: services.length,
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 4,
          childAspectRatio: 0.9,
          crossAxisSpacing: 10,
          mainAxisSpacing: 10,
        ),
        itemBuilder: (context, index) {
          final service = services[index];
          return GestureDetector(
            onTap: () => print('Navigasi ke ${service.title} Katalog'), // Navigasi ke L, M, N
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: service.color.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Icon(service.icon, color: service.color, size: 28),
                ),
                const SizedBox(height: 5),
                Text(service.title, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600), textAlign: TextAlign.center),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildPromoSection() {
    // J. Promo (Horizontal Scroll Banners)
    return FutureBuilder<List<PromoModel>>(
      future: _dataService.getActivePromotions(),
      builder: (context, snapshot) {
        if (!snapshot.hasData || snapshot.data!.isEmpty) return const SizedBox.shrink();
        
        final promos = snapshot.data!;
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Padding(
              padding: EdgeInsets.only(left: 16.0, top: 10.0, bottom: 8.0),
              child: Text('Promo Spesial Untukmu', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            ),
            SizedBox(
              height: 150,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: promos.length,
                itemBuilder: (context, index) {
                  final promo = promos[index];
                  return Container(
                    width: MediaQuery.of(context).size.width * 0.75,
                    margin: const EdgeInsets.only(right: 15),
                    padding: const EdgeInsets.all(15),
                    decoration: BoxDecoration(
                      color: promo.color,
                      borderRadius: BorderRadius.circular(15),
                      boxShadow: [BoxShadow(color: promo.color.withOpacity(0.3), blurRadius: 5)],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(promo.title, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 5),
                        Text(promo.subtitle, style: const TextStyle(color: Colors.white70, fontSize: 14)),
                        const Spacer(),
                        const Text('Klaim Sekarang >', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 20),
          ],
        );
      },
    );
  }

  Widget _buildDiscoverySection(String title) {
    // Contoh untuk widget penemuan (discovery widgets)
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 10),
          child: Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        ),
        SizedBox(
          height: 120,
          child: ListView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16),
            children: [
              _buildDiscoveryCard('Restoran B', Icons.lunch_dining),
              _buildDiscoveryCard('Motor Terdekat', Icons.two_wheeler),
              _buildDiscoveryCard('Promo Bills', Icons.payment),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildDiscoveryCard(String title, IconData icon) {
    return Container(
      width: 100,
      margin: const EdgeInsets.only(right: 12),
      child: Column(
        children: [
          Container(
            height: 70,
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(10),
              boxShadow: [BoxShadow(color: Colors.grey.shade200, blurRadius: 5)],
            ),
            child: Center(child: Icon(icon, size: 40, color: Colors.blueGrey)),
          ),
          const SizedBox(height: 5),
          Text(title, style: const TextStyle(fontSize: 12), textAlign: TextAlign.center),
        ],
      ),
    );
  }
}


/// =======================================================================
/// 2. UNIVERSAL SEARCH SCREEN (Z, Z2)
/// =======================================================================
class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final TextEditingController _searchController = TextEditingController();
  final DataService _dataService = DataService();
  String _query = '';
  
  // Z. Search_Recent Search
  final List<String> _recentSearches = ['Nasi Padang', 'Ojek ke Stasiun', 'Reset PIN'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        // Z. Search
        automaticallyImplyLeading: false, // Hapus tombol back default
        title: TextField(
          controller: _searchController,
          autofocus: true,
          onChanged: (value) {
            setState(() {
              _query = value.toLowerCase();
            });
          },
          decoration: InputDecoration(
            hintText: 'Cari produk, layanan, atau bantuan...',
            border: InputBorder.none,
            prefixIcon: const Icon(Icons.search, color: Colors.grey),
            suffixIcon: _query.isNotEmpty
                ? IconButton(
                    icon: const Icon(Icons.clear, color: Colors.grey),
                    onPressed: () {
                      _searchController.clear();
                      setState(() {
                        _query = '';
                      });
                    },
                  )
                : null,
          ),
        ),
        backgroundColor: Colors.white,
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Batal', style: TextStyle(color: Colors.teal)),
          )
        ],
      ),
      body: _query.isEmpty ? _buildRecentSearches() : _buildSearchResults(),
    );
  }
  
  // Tampilan ketika belum ada query
  Widget _buildRecentSearches() {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Pencarian Terbaru', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                TextButton(onPressed: () => setState(() => _recentSearches.clear()), child: const Text('Hapus Semua', style: TextStyle(color: Colors.red))),
              ],
            ),
          ),
          ..._recentSearches.map((term) => ListTile(
            leading: const Icon(Icons.history, color: Colors.grey),
            title: Text(term),
            onTap: () {
              _searchController.text = term;
              setState(() => _query = term.toLowerCase());
            },
          )),
          const Divider(),
          // Kategori Layanan Cepat
          _buildCategoryChips(),
        ],
      ),
    );
  }

  Widget _buildCategoryChips() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.only(left: 16.0, top: 10, bottom: 5),
          child: Text('Jelajahi Kategori', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0),
          child: Wrap(
            spacing: 8.0,
            children: _dataService.getCoreServices().map((service) => Chip(
              label: Text(service.title),
              backgroundColor: service.color.withOpacity(0.1),
              onDeleted: () => print('Filter Kategori: ${service.title}'),
              deleteIcon: Icon(service.icon, size: 16, color: Colors.grey),
            )).toList(),
          ),
        )
      ],
    );
  }

  // Tampilan ketika ada query
  Widget _buildSearchResults() {
    // Logika Pencarian Universal: Menggabungkan hasil dari berbagai sumber
    final products = _dataService.getProductList().where((p) => p.toLowerCase().contains(_query)).toList();
    final helpTopics = _dataService.getHelpTopics().where((h) => h.toLowerCase().contains(_query)).toList();

    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (products.isNotEmpty) _buildResultSection('Produk dan Layanan', products, Icons.shopping_bag),
          if (helpTopics.isNotEmpty) _buildResultSection('Pusat Bantuan', helpTopics, Icons.help_outline), // Z2. Help Center
          
          if (products.isEmpty && helpTopics.isEmpty)
            const Center(
              // Z. Search_Not Found
              child: Padding(
                padding: EdgeInsets.only(top: 50.0),
                child: Text('Tidak ada hasil yang ditemukan.', style: TextStyle(color: Colors.grey)),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildResultSection(String title, List<String> results, IconData icon) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 10),
          child: Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.teal)),
        ),
        ...results.map((result) => ListTile(
          leading: Icon(icon, color: Colors.teal),
          title: Text(result),
          onTap: () => print('Membuka detail untuk: $result'),
        )),
        const Divider(),
      ],
    );
  }
}
