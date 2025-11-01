import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:myapp/providers/review_provider.dart';
import 'package:myapp/models/review_model.dart';
import 'package:go_router/go_router.dart';

class RatingScreen extends StatefulWidget {
  final String restaurantId;

  const RatingScreen({super.key, required this.restaurantId});

  @override
  _RatingScreenState createState() => _RatingScreenState();
}

class _RatingScreenState extends State<RatingScreen> {
  double _rating = 0;
  final _commentController = TextEditingController();

  Future<void> _submitReview() async {
    if (_rating > 0 && _commentController.text.isNotEmpty) {
      final user = FirebaseAuth.instance.currentUser;
      if (user == null) return;

      final newReview = Review(
        id: ' ', // The backend will generate the ID
        restaurantId: widget.restaurantId,
        userName: user.displayName ?? 'Anonymous User',
        rating: _rating,
        comment: _commentController.text,
        timestamp: DateTime.now(), // The backend will handle the timestamp
      );

      await Provider.of<ReviewProvider>(
        context,
        listen: false,
      ).submitReview(newReview);

      if (mounted) {
        context.pop(); // Go back to the previous page after submitting
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Beri Ulasan')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Beri rating untuk restoran ini',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 10),
            _buildStarRating(),
            const SizedBox(height: 20),
            TextField(
              controller: _commentController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Tulis ulasan Anda...',
              ),
              maxLines: 4,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _submitReview,
              child: const Text('Kirim Ulasan'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStarRating() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: List.generate(5, (index) {
        return IconButton(
          icon: Icon(
            index < _rating ? Icons.star : Icons.star_border,
            color: Colors.amber,
          ),
          onPressed: () {
            setState(() {
              _rating = index + 1.0;
            });
          },
        );
      }),
    );
  }
}
