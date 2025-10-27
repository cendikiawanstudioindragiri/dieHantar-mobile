import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:myapp/services/firebase_service.dart';

class HomeResultScreen extends StatelessWidget {
  final String orderId;

  const HomeResultScreen({super.key, required this.orderId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Order Status'),
      ),
      body: StreamProvider<OrderModel?>.value(
        value: context.read<OrderService>().streamOrderDetails(orderId),
        initialData: null,
        child: Consumer<OrderModel?>(
          builder: (context, order, child) {
            if (order == null) {
              return const Center(child: CircularProgressIndicator());
            }
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('Order ID: ${order.id}'),
                  Text('Status: ${order.status}'),
                  Text('Total: ${order.totalAmount}'),
                  Text('Address: ${order.deliveryAddress}'),
                  Text('Created At: ${order.createdAt}'),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
