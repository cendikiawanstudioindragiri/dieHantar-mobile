class Review {
  final String id;
  final String restaurantId; // Untuk mengasosiasikan ulasan dengan restoran
  final String userName;
  final double rating; // Rating bintang (1-5)
  final String comment;
  final DateTime timestamp;

  Review({
    required this.id,
    required this.restaurantId,
    required this.userName,
    required this.rating,
    required this.comment,
    required this.timestamp,
  });
}
