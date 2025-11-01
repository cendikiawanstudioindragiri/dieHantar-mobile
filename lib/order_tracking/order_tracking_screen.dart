import 'dart:developer' as developer;
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:myapp/models/order_model.dart';
import 'package:myapp/services/firebase_service.dart';

const Map<String, String> orderStatuses = {
  'PENDING_PAYMENT': 'Menunggu Pembayaran',
  'PROCESSING': 'Pesanan Diproses oleh Toko',
  'DRIVER_SEARCHING': 'Mencari Driver',
  'DRIVER_EN_ROUTE': 'Driver Menuju Lokasi Ambil',
  'PICKED_UP': 'Pesanan Diambil Driver',
  'DELIVERING': 'Driver Menuju Lokasi Anda',
  'DELIVERED': 'Pesanan Berhasil Dikirim',
  'CANCELED': 'Pesanan Dibatalkan',
  'REFUNDED': 'Dana Dikembalikan',
};

class OrderTrackingScreen extends StatefulWidget {
  final String orderId;

  const OrderTrackingScreen({super.key, required this.orderId});

  @override
  State<OrderTrackingScreen> createState() => _OrderTrackingScreenState();
}

class _OrderTrackingScreenState extends State<OrderTrackingScreen> {
  final OrderService _orderService = OrderService();

  final List<String> trackingSteps = [
    orderStatuses['PROCESSING']!,
    orderStatuses['DRIVER_SEARCHING']!,
    orderStatuses['PICKED_UP']!,
    orderStatuses['DELIVERING']!,
    orderStatuses['DELIVERED']!,
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Lacak Pesanan'),
        backgroundColor: Colors.teal,
        elevation: 0,
      ),
      body: StreamBuilder<OrderModel>(
        stream: _orderService.streamOrderDetails(widget.orderId),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Terjadi kesalahan: ${snapshot.error}'));
          }
          if (!snapshot.hasData) {
            return const Center(child: Text('Pesanan tidak ditemukan.'));
          }

          final order = snapshot.data!;
          final currentStatus = order.status;

          if (currentStatus == orderStatuses['CANCELED']) {
            return _buildCanceledOrDeliveredView(
              'Pesanan Dibatalkan',
              Colors.red,
              'Mohon maaf, pesanan ini telah dibatalkan.',
              Icons.cancel_outlined,
            );
          }

          if (currentStatus == orderStatuses['DELIVERED']) {
            return _buildCanceledOrDeliveredView(
              'Pesanan Selesai',
              Colors.green,
              'Terima kasih telah menggunakan dieHantar! Jangan lupa berikan Rating.',
              Icons.check_circle_outline,
              showRatingButton: true,
            );
          }

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildStatusHeader(order.id, currentStatus),
                const SizedBox(height: 20),
                _buildTrackingTimeline(currentStatus),
                const SizedBox(height: 30),
                const Divider(),
                _buildDriverContactCard(order.id),
                const SizedBox(height: 20),
                _buildDeliveryAddress(order.deliveryAddress),
                const SizedBox(height: 20),
                _buildSummary(order),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildStatusHeader(String orderId, String status) {
    return Card(
      elevation: 4,
      color: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'No. Pesanan: $orderId',
              style: const TextStyle(fontSize: 16, color: Colors.grey),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                const Icon(Icons.delivery_dining, size: 30, color: Colors.teal),
                const SizedBox(width: 10),
                Flexible(
                  child: Text(
                    status,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: Colors.teal,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 5),
            Text(
              'Status terakhir diperbarui: ${DateTime.now().toLocal().toString().substring(11, 16)}',
              style: const TextStyle(fontSize: 12, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTrackingTimeline(String currentStatus) {
    return Column(
      children: trackingSteps.map((step) {
        final index = trackingSteps.indexOf(step);
        final currentIndex = trackingSteps.indexOf(currentStatus);

        final isCompleted = currentIndex >= index;
        final isCurrent = currentIndex == index;

        return Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Column(
              children: [
                Container(
                  width: 24,
                  height: 24,
                  decoration: BoxDecoration(
                    color: isCompleted ? Colors.teal : Colors.grey[300],
                    shape: BoxShape.circle,
                    border: isCurrent
                        ? Border.all(color: Colors.teal, width: 3)
                        : null,
                  ),
                  child: isCompleted
                      ? const Icon(Icons.check, color: Colors.white, size: 14)
                      : null,
                ),
                if (index < trackingSteps.length - 1)
                  Container(
                    width: 2,
                    height: 40,
                    color: isCompleted ? Colors.teal : Colors.grey[300],
                  ),
              ],
            ),
            const SizedBox(width: 10),
            Padding(
              padding: const EdgeInsets.only(top: 4.0),
              child: Text(
                step,
                style: TextStyle(
                  fontWeight: isCompleted ? FontWeight.bold : FontWeight.normal,
                  color: isCompleted ? Colors.black87 : Colors.grey,
                ),
              ),
            ),
          ],
        );
      }).toList(),
    );
  }

  Widget _buildDriverContactCard(String orderId) {
    const driverName = "Budi Santoso";
    const licensePlate = "BP 1234 XY";

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Driver Anda',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.teal,
              ),
            ),
            const Divider(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    const CircleAvatar(
                      backgroundColor: Colors.teal,
                      child: Icon(Icons.person, color: Colors.white),
                    ),
                    const SizedBox(width: 10),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          driverName,
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                        Text(
                          licensePlate,
                          style: const TextStyle(
                            fontSize: 12,
                            color: Colors.grey,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
                Row(
                  children: [
                    IconButton(
                      icon: const Icon(Icons.message, color: Colors.blue),
                      onPressed: () => contactDriver('Message', orderId),
                      tooltip: 'Pesan',
                    ),
                    IconButton(
                      icon: const Icon(Icons.call, color: Colors.green),
                      onPressed: () => contactDriver('Call', orderId),
                      tooltip: 'Telepon',
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDeliveryAddress(String address) {
    return Card(
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: ListTile(
        leading: const Icon(Icons.location_on, color: Colors.red),
        title: const Text(
          'Alamat Pengiriman',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        subtitle: Text(address),
      ),
    );
  }

  Widget _buildSummary(OrderModel order) {
    return Card(
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              'Total Pembayaran:',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            Text(
              'Rp ${order.totalAmount.toString()}',
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.redAccent,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCanceledOrDeliveredView(
    String title,
    Color color,
    String message,
    IconData icon, {
    bool showRatingButton = false,
  }) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 80, color: color),
            const SizedBox(height: 20),
            Text(
              title,
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            const SizedBox(height: 10),
            Text(
              message,
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16, color: Colors.grey[700]),
            ),
            const SizedBox(height: 30),
            if (showRatingButton)
              ElevatedButton(
                onPressed: () => context.go(
                  '/rating',
                  extra: 'restaurant_id_placeholder',
                ), // Ganti dengan ID restoran yang sebenarnya
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.amber,
                  padding: const EdgeInsets.symmetric(
                    horizontal: 40,
                    vertical: 15,
                  ),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
                child: const Text(
                  'Beri Ulasan',
                  style: TextStyle(fontSize: 16, color: Colors.white),
                ),
              ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () => context.go('/home'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.teal,
                padding: const EdgeInsets.symmetric(
                  horizontal: 40,
                  vertical: 15,
                ),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
              child: const Text(
                'Kembali ke Home',
                style: TextStyle(fontSize: 16, color: Colors.white),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void contactDriver(String type, String orderId) {
    // Panggil Cloud Function
    developer.log(
      'Memanggil Cloud Function untuk $type Driver di Order $orderId',
    );
  }
}
