import 'dart:async';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:myapp/common/commons_widgets.dart';
import 'package:myapp/models/order_model.dart';
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';

class AuthService with ChangeNotifier {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  User? currentUser;

  AuthService() {
    _auth.authStateChanges().listen((user) {
      currentUser = user;
      notifyListeners();
    });
  }

  Stream<User?> get authStateChanges => _auth.authStateChanges();

  Future<void> signOut() async {
    await _auth.signOut();
  }
}

class OrderService {
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

class DataService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  Stream<List<LocationModel>> userLocationsStream(String userId) {
    // Implement actual logic to fetch user locations from Firestore
    return Stream.value([]);
  }

  Future<void> addUserLocation(String userId, LocationModel location) async {
    // Implement actual logic to add user location to Firestore
  }
}
