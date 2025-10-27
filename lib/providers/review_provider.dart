import 'package:flutter/foundation.dart';
import 'package:myapp/models/review_model.dart';

class ReviewProvider with ChangeNotifier {
  // Menggunakan Map untuk menyimpan ulasan berdasarkan ID restoran
  final Map<String, List<Review>> _reviews = {};

  Map<String, List<Review>> get reviews => _reviews;

  // Mendapatkan ulasan untuk restoran tertentu
  List<Review> getReviewsForRestaurant(String restaurantId) {
    return _reviews[restaurantId] ?? [];
  }

  // Menambahkan ulasan baru
  void addReview(Review review) {
    if (!_reviews.containsKey(review.restaurantId)) {
      _reviews[review.restaurantId] = [];
    }
    _reviews[review.restaurantId]!.add(review);
    notifyListeners();
  }
}
