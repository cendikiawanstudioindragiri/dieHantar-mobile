class Restaurant {
  final String id;
  final String name;
  final String cuisine;
  final double rating;
  final String distance;
  final String imageUrl;

  Restaurant({
    required this.id,
    required this.name,
    required this.cuisine,
    required this.rating,
    required this.distance,
    required this.imageUrl,
  });

  factory Restaurant.fromJson(Map<String, dynamic> json) {
    return Restaurant(
      id: json['id'],
      name: json['name'],
      cuisine: json['cuisine'],
      rating: (json['rating'] as num).toDouble(),
      distance: json['distance'],
      imageUrl: json['imageUrl'],
    );
  }
}
