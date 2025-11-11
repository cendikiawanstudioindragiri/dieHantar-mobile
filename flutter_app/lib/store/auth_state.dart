import 'package:flutter/foundation.dart';
import '../services/api_service.dart';
import '../models/user_model.dart';

class AuthState extends ChangeNotifier {
  final ApiService _api;
  User? _user;
  String? _token;
  bool _loading = false;
  String? _error;

  AuthState({ApiService? api}) : _api = api ?? ApiService();

  User? get user => _user;
  String? get token => _token;
  bool get isAuthenticated => _token != null && _user != null;
  bool get isLoading => _loading;
  String? get error => _error;

  Future<void> register({required String email, required String password, String? fullName}) async {
    _setLoading(true);
    _error = null;
    try {
      final created = await _api.registerUser(email: email, password: password, fullName: fullName);
  final t = await _api.login(email: email, password: password);
  _token = t;
  _api.setAuthToken(t);
      // Fetch enriched profile if needed
      _user = created;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    } finally {
      _setLoading(false);
    }
  }

  Future<void> login({required String email, required String password}) async {
    _setLoading(true);
    _error = null;
    try {
  final t = await _api.login(email: email, password: password);
  _token = t;
  _api.setAuthToken(t);
      _user = await _api.me();
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    } finally {
      _setLoading(false);
    }
  }

  void logout() {
    _token = null;
    _user = null;
    _error = null;
    _api.setAuthToken(null);
    notifyListeners();
  }

  void _setLoading(bool v) {
    _loading = v;
    notifyListeners();
  }
}
