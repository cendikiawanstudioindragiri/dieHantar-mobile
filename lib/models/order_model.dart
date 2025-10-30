import 'package:cloud_firestore/cloud_firestore.dart';

class OrderModel {
  final String id;
  final String userId;
  final List<Map<String, dynamic>> items;
  final double totalAmount;
  final String deliveryAddress;
  final String status;
  final Timestamp createdAt;

  OrderModel({
    required this.id,
    required this.userId,
    required this.items,
    required this.totalAmount,
    required this.deliveryAddress,
    required this.status,
    required this.createdAt,
  });

  factory OrderModel.fromFirestore(DocumentSnapshot doc) {
    Map data = doc.data() as Map<String, dynamic>;
    return OrderModel(
      id: doc.id,
      userId: data['userId'] ?? '',
      items: List<Map<String, dynamic>>.from(data['items'] ?? []),
      totalAmount: (data['totalAmount'] ?? 0).toDouble(),
      deliveryAddress: data['deliveryAddress'] ?? '',
      status: data['status'] ?? 'Pending',
      createdAt: data['createdAt'] ?? Timestamp.now(),
    );
  }
}
