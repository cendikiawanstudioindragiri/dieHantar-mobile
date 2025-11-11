import 'package:flutter/foundation.dart';
import '../models/user_model.dart';
import '../services/api_service.dart';

/// Simple auth state holder for Flutter app
/// Responsibilities:
/// - Hold authenticated [User] and JWT token
/// - Provide methods to update/clear auth state
/// - Apply token to [ApiService] when updated
class UserProvider extends ChangeNotifier {
  User? _user;
  String? _token;

  final ApiService api;

  UserProvider({required this.api});

  User? get user => _user;
  String? get token => _token;
  bool get isAuthenticated => _token != null && _token!.isNotEmpty;

  /// Set token and optionally user, then notify listeners.
  void setAuth({String? token, User? user}) {
    if (token != null) {
      _token = token;
      api.setAuthToken(token);
    }
    if (user != null) {
      _user = user;
    }
    notifyListeners();
  }

  /// Clear token and user (logout)
  void clear() {
    _token = null;
    _user = null;
    api.setAuthToken(null);
    notifyListeners();
  }

  /// Helper to set the current user profile
  void setUser(User user) {
    _user = user;
    notifyListeners();
  }
}
