import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:myapp/models/order_model.dart';

class AuthService with ChangeNotifier {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  User? get currentUser => _auth.currentUser;

  Stream<User?> get authStateChanges => _auth.authStateChanges();

  Future<void> signInWithEmailAndPassword({
    required String email,
    required String password,
  }) async {
    await _auth.signInWithEmailAndPassword(email: email, password: password);
    notifyListeners();
  }

  Future<void> signOut() async {
    await _auth.signOut();
    notifyListeners();
  }
}

class OrderService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  Stream<OrderModel?> streamOrderDetails(String orderId) {
    return _firestore
        .collection('orders')
        .doc(orderId)
        .snapshots()
        .map((snap) => snap.exists ? OrderModel.fromFirestore(snap) : null);
  }
}

class DataService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  Stream<QuerySnapshot> userLocationsStream() {
    return _firestore.collection('user_locations').snapshots();
  }

  Future<void> addUserLocation(Map<String, dynamic> locationData) {
    return _firestore.collection('user_locations').add(locationData);
  }
}
