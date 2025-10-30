import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:myapp/services/firebase_service.dart';

enum OrderStatus { ongoing, completed, cancelled }

class PaymentService {
  Future<int> getWalletBalance(String uid) async => 150000; // Contoh saldo
  Future<List<Map<String, dynamic>>> getTransactionHistory(String uid) async => [
    {'date': '10 Jun', 'desc': 'Bayar Pesanan #101', 'amount': -45000, 'type': 'debit'},
    {'date': '09 Jun', 'desc': 'Top Up Dana', 'amount': 100000, 'type': 'credit'},
  ];
}


/// =======================================================================
/// 1. SCREEN DOMPET/PEMBAYARAN (S. Payment Methods, Top Up)
/// =======================================================================
class WalletScreen extends StatelessWidget {
  final PaymentService _paymentService = PaymentService();
  final String userId = FirebaseAuth.instance.currentUser?.uid ?? 'dummy_uid';

  WalletScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('dieHantar Pay (S. Payment Methods)'),
        backgroundColor: Colors.teal,
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildBalanceCard(),
            _buildWalletActions(context),
            const Divider(height: 1),
            _buildTransactionHistory(),
          ],
        ),
      ),
    );
  }

  Widget _buildBalanceCard() {
    return FutureBuilder<int>(
      future: _paymentService.getWalletBalance(userId),
      builder: (context, snapshot) {
        final balance = snapshot.data ?? 0;
        return Container(
          padding: const EdgeInsets.all(20),
          margin: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.teal,
            borderRadius: BorderRadius.circular(15),
            boxShadow: [
              BoxShadow(color: Colors.teal.shade300, blurRadius: 10),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Saldo dieHantar Pay', style: TextStyle(color: Colors.white, fontSize: 16)),
              const SizedBox(height: 5),
              Text(
                'Rp ${balance.toString()}',
                style: const TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              const Text(
                'Metode Pembayaran Lain: Debit/Kredit, Bank Transfer', // S. Payment Methods
                style: TextStyle(color: Colors.white70, fontSize: 12),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildWalletActions(BuildContext context) {
    // S. Payment Methods_Top Up_Typing amount
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildActionButton(
            context,
            icon: Icons.add_circle_outline,
            label: 'Top Up',
            onTap: () => print('Navigasi ke Top Up Screen (S. Payment Methods_Top Up)'),
          ),
          _buildActionButton(
            context,
            icon: Icons.send_outlined,
            label: 'Transfer',
            onTap: () => print('Navigasi ke Transfer Saldo'),
          ),
          _buildActionButton(
            context,
            icon: Icons.history,
            label: 'History',
            onTap: () => print('Lihat Riwayat Transaksi'),
          ),
        ],
      ),
    );
  }

  Widget _buildActionButton(BuildContext context, {required IconData icon, required String label, required VoidCallback onTap}) {
    return InkWell(
      onTap: onTap,
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: Colors.teal.withOpacity(0.1),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(icon, color: Colors.teal),
          ),
          const SizedBox(height: 4),
          Text(label, style: const TextStyle(fontSize: 12)),
        ],
      ),
    );
  }

  Widget _buildTransactionHistory() {
    return FutureBuilder<List<Map<String, dynamic>>>(
      future: _paymentService.getTransactionHistory(userId),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: Padding(
            padding: EdgeInsets.all(20.0),
            child: CircularProgressIndicator(color: Colors.teal),
          ));
        }

        final history = snapshot.data ?? [];
        return Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Riwayat Transaksi', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 10),
              ...history.map((tx) => ListTile(
                leading: Icon(
                  tx['type'] == 'debit' ? Icons.arrow_upward : Icons.arrow_downward,
                  color: tx['type'] == 'debit' ? Colors.redAccent : Colors.green,
                ),
                title: Text(tx['desc']),
                subtitle: Text(tx['date']),
                trailing: Text(
                  'Rp ${tx['amount'].abs()}',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: tx['type'] == 'debit' ? Colors.redAccent : Colors.green,
                  ),
                ),
              )),
              if (history.isEmpty) const Text("Belum ada riwayat transaksi."),
            ],
          ),
        );
      },
    );
  }
}


/// =======================================================================
/// 2. SCREEN RIWAYAT PESANAN (V. My Order_All)
/// =======================================================================
class OrderHistoryScreen extends StatefulWidget {
  const OrderHistoryScreen({super.key});

  @override
  State<OrderHistoryScreen> createState() => _OrderHistoryScreenState();
}

class _OrderHistoryScreenState extends State<OrderHistoryScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final OrderService _orderService = OrderService();
  final String userId = FirebaseAuth.instance.currentUser?.uid ?? 'dummy_uid';

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Riwayat Pesanan (V. My Order_All)'),
        backgroundColor: Colors.teal,
        bottom: TabBar( // V. My Order_All tabs
          controller: _tabController,
          indicatorColor: Colors.white,
          tabs: const [
            Tab(text: 'Berjalan'),
            Tab(text: 'Selesai'),
            Tab(text: 'Dibatalkan'),
          ],
        ),
      ),
      body: FutureBuilder<List<OrderModel>>(
        future: null, // Replace with your future
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator(color: Colors.teal));
          }
          if (snapshot.hasError || !snapshot.hasData) {
            return const Center(child: Text("Gagal memuat riwayat pesanan."));
          }

          final orders = snapshot.data!;
          final ongoing = orders.where((o) => o.status == "ongoing").toList();
          final completed = orders.where((o) => o.status == "completed").toList();
          final cancelled = orders.where((o) => o.status == "cancelled").toList();

          return TabBarView(
            controller: _tabController,
            children: [
              _buildOrderList(ongoing, OrderStatus.ongoing),
              _buildOrderList(completed, OrderStatus.completed),
              _buildOrderList(cancelled, OrderStatus.cancelled),
            ],
          );
        },
      ),
    );
  }

  Widget _buildOrderList(List<OrderModel> orders, OrderStatus filterStatus) {
    if (orders.isEmpty) {
      return Center(
        child: Text(
          filterStatus == OrderStatus.ongoing ? 'Tidak ada pesanan aktif.' : 'Tidak ada riwayat di kategori ini.',
          style: const TextStyle(color: Colors.grey),
        ),
      );
    }
    
    return ListView.builder(
      itemCount: orders.length,
      itemBuilder: (context, index) {
        final order = orders[index];
        return Card(
          margin: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
          elevation: 2,
          child: ListTile(
            leading: Icon(
              filterStatus == OrderStatus.ongoing ? Icons.delivery_dining : filterStatus == OrderStatus.completed ? Icons.check_circle : Icons.cancel,
              color: filterStatus == OrderStatus.ongoing ? Colors.blue : filterStatus == OrderStatus.completed ? Colors.green : Colors.red,
            ),
            title: Text(order.orderId, style: const TextStyle(fontWeight: FontWeight.bold)),
            subtitle: Text('ID: ${order.orderId} | Tgl: ${order.createdAt.day}/${order.createdAt.month}'),
            trailing: Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('Rp ${order.totalAmount}', style: const TextStyle(fontWeight: FontWeight.bold)),
                Text(order.status.toUpperCase(), style: TextStyle(fontSize: 10, color: filterStatus == OrderStatus.ongoing ? Colors.blue : Colors.black54)),
              ],
            ),
            onTap: () => print('Lihat detail pesanan ${order.orderId}'),
          ),
        );
      },
    );
  }
}


/// =======================================================================
/// 3. SCREEN PROFIL & PENGATURAN (Y. Profile, F. Set PIN, G. Touch ID)
/// =======================================================================
class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  // Simulasi data user
  final UserModel currentUser = UserModel(uid: 'user123', isPinSet: true, phoneNumber: '', fullName: 'fullName');
  bool isTouchIdEnabled = false; // Status G. Set Touch ID

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profil Saya (Y. Profile)'),
        backgroundColor: Colors.teal,
        actions: [
          IconButton(
            icon: const Icon(Icons.logout), 
            onPressed: () => print('Logout User'),
            tooltip: 'Logout',
          )
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildProfileHeader(),
            const Divider(),
            _buildAccountSettings(context),
            const Divider(height: 1),
            _buildSecuritySettings(context),
            const Divider(height: 1),
            _buildGeneralSettings(context),
          ],
        ),
      ),
    );
  }

  Widget _buildProfileHeader() {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Row(
        children: [
          const CircleAvatar(
            radius: 40,
            backgroundColor: Colors.teal,
            child: Icon(Icons.person, size: 40, color: Colors.white),
          ),
          const SizedBox(width: 20),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(currentUser.fullName ?? '', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              Text(currentUser.phoneNumber, style: const TextStyle(color: Colors.grey)),
              Text(currentUser.email ?? '', style: const TextStyle(color: Colors.grey)),
            ],
          ),
        ],
      ),
    );
  }
  
  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 16.0, top: 16.0, bottom: 8.0),
      child: Text(
        title.toUpperCase(),
        style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.teal, fontSize: 13),
      ),
    );
  }

  Widget _buildAccountSettings(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildSectionTitle('Akun'),
        ListTile(
          leading: const Icon(Icons.edit, color: Colors.orange),
          title: const Text('Edit Profil (E. Set Your Profile)'),
          onTap: () => print('Navigasi ke Edit Profil'),
        ),
        ListTile(
          leading: const Icon(Icons.payment, color: Colors.blue),
          title: const Text('Metode Pembayaran (S. Payment Methods)'),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => WalletScreen())),
        ),
        ListTile(
          leading: const Icon(Icons.location_on_outlined, color: Colors.green),
          title: const Text('Alamat Tersimpan (I. My locations)'),
          onTap: () => print('Navigasi ke Pengaturan Lokasi'),
        ),
        ListTile(
          leading: const Icon(Icons.favorite_border, color: Colors.red),
          title: const Text('Daftar Item Favorit (W. Liked)'),
          onTap: () => print('Navigasi ke Favorit'),
        ),
      ],
    );
  }
  
  Widget _buildSecuritySettings(BuildContext context) {
    // F. Set PIN Security & G. Set Touch ID Security
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildSectionTitle('Keamanan'),
        ListTile(
          leading: Icon(currentUser.isPinSet ? Icons.lock : Icons.lock_open, color: Colors.purple),
          title: Text(currentUser.isPinSet ? 'Ubah PIN Keamanan' : 'Atur PIN Keamanan (F. Set PIN Security)'),
          trailing: Text(currentUser.isPinSet ? 'Set' : 'Belum Set'),
          onTap: () => print('Navigasi ke Pengaturan/Ubah PIN'), // F. PIN typing
        ),
        SwitchListTile(
          secondary: const Icon(Icons.fingerprint, color: Colors.blueGrey),
          title: const Text('Akses Touch ID / Biometrik (G. Touch ID Security)'),
          value: isTouchIdEnabled,
          onChanged: (bool value) {
            setState(() {
              isTouchIdEnabled = value;
              print('Status Touch ID: $isTouchIdEnabled');
              // Logika Biometrik harus dilakukan di sini
            });
          },
        ),
      ],
    );
  }

  Widget _buildGeneralSettings(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildSectionTitle('Lainnya'),
        // Z2. Help center
        ListTile(leading: const Icon(Icons.help_outline), title: const Text('Pusat Bantuan'), onTap: () => print('Navigasi ke Help Center (Z2)')), 
        // Z3. Others_Terms of Service, Z3. Others_Privacy Policy
        ListTile(leading: const Icon(Icons.policy), title: const Text('Syarat & Ketentuan'), onTap: () => print('Navigasi ke Syarat & Ketentuan (Z3)')),
        ListTile(leading: const Icon(Icons.info_outline), title: const Text('Tentang Aplikasi'), onTap: () => print('Navigasi ke Tentang Aplikasi')),
        // Z1. Invite friends
        ListTile(leading: const Icon(Icons.share_outlined), title: const Text('Undang Teman'), onTap: () => print('Share Link Undangan (Z1)')),
      ],
    );
  }
}