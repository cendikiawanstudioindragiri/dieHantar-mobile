import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:firebase_auth/firebase_auth.dart';
import 'package:myapp/models/review_model.dart';

class ReviewProvider with ChangeNotifier {
  final Map<String, List<Review>> _reviews = {};
  final String _baseUrl =
      'https://us-central1-YOUR_PROJECT_ID.cloudfunctions.net'; // TODO: Replace with your actual base URL

  Map<String, List<Review>> get reviews => _reviews;

  Future<void> getReviewsForRestaurant(String restaurantId) async {
    final url = Uri.parse('$_baseUrl/reviewsAPI?restaurantId=$restaurantId');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success']) {
          final List<dynamic> reviewData = data['reviews'];
          _reviews[restaurantId] = reviewData
              .map((json) => Review.fromJson(json))
              .toList();
          notifyListeners();
        }
      }
    } catch (e) {
      // Handle error
    }
  }

  Future<void> submitReview(Review review) async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return; // Not authenticated

    final idToken = await user.getIdToken();
    final url = Uri.parse('$_baseUrl/reviewsAPI');

    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $idToken',
        },
        body: json.encode(review.toJson()),
      );

      if (response.statusCode == 201) {
        // Successfully submitted, now refresh the reviews
        getReviewsForRestaurant(review.restaurantId);
      }
    } catch (e) {
      // Handle error
    }
  }
}
