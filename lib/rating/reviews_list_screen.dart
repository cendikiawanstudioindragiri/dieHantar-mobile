import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:myapp/providers/review_provider.dart';
import 'package:myapp/models/review_model.dart';

class ReviewsListScreen extends StatelessWidget {
  final String restaurantId;

  const ReviewsListScreen({super.key, required this.restaurantId});

  @override
  Widget build(BuildContext context) {
    final reviewProvider = Provider.of<ReviewProvider>(context);
    final reviews = reviewProvider.getReviewsForRestaurant(restaurantId);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Ulasan Pelanggan'),
      ),
      body: reviews.isEmpty
          ? const Center(
              child: Text('Belum ada ulasan untuk restoran ini.'),
            )
          : ListView.builder(
              itemCount: reviews.length,
              itemBuilder: (ctx, i) => _buildReviewItem(context, reviews[i]),
            ),
    );
  }

  Widget _buildReviewItem(BuildContext context, Review review) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 15, vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(review.userName, style: const TextStyle(fontWeight: FontWeight.bold)),
                Text(
                  '${review.timestamp.day}/${review.timestamp.month}/${review.timestamp.year}',
                  style: const TextStyle(color: Colors.grey, fontSize: 12),
                ),
              ],
            ),
            const SizedBox(height: 5),
            _buildStarRating(review.rating),
            const SizedBox(height: 8),
            Text(review.comment),
          ],
        ),
      ),
    );
  }

  Widget _buildStarRating(double rating) {
    return Row(
      children: List.generate(5, (index) {
        return Icon(
          index < rating ? Icons.star : Icons.star_border,
          color: Colors.amber,
          size: 16,
        );
      }),
    );
  }
}
