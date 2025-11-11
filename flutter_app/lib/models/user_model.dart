class User {
  final int id;
  final String email;
  final String? fullName;
  final bool isActive;
  final String? phoneNumber;
  final DateTime? createdAt;

  User({
    required this.id,
    required this.email,
    this.fullName,
    required this.isActive,
    this.phoneNumber,
    this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      email: json['email'] as String,
      fullName: json['full_name'] as String?,
      isActive: json['is_active'] as bool? ?? true,
      phoneNumber: json['phone_number'] as String?,
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'] as String)
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      if (fullName != null) 'full_name': fullName,
      'is_active': isActive,
      if (phoneNumber != null) 'phone_number': phoneNumber,
      if (createdAt != null) 'created_at': createdAt!.toIso8601String(),
    };
  }
}
