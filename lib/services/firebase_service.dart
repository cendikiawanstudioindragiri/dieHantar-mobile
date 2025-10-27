import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:myapp/models/user_model.dart';

class FirebaseService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  Stream<OrderModel> streamOrderDetails(String orderId) {
    return _firestore.collection('orders').doc(orderId).snapshots().map((snapshot) {
      if (snapshot.exists) {
        return OrderModel.fromFirestore(snapshot);
      } else {
        throw Exception('Pesanan tidak ditemukan');
      }
    });
  }
}
