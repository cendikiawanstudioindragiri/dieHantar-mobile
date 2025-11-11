import 'package:dio/dio.dart';
import '../models/user_model.dart';

class ApiException implements Exception {
  final String message;
  final int? statusCode;
  final dynamic data;
  ApiException(this.message, {this.statusCode, this.data});

  @override
  String toString() => 'ApiException($statusCode): $message';
}

class ApiService {
  final Dio _dio;
  String? _token;

  ApiService({String? baseUrl})
      : _dio = Dio(
          BaseOptions(
            baseUrl: baseUrl ?? 'http://127.0.0.1:8000',
            connectTimeout: const Duration(seconds: 10),
            receiveTimeout: const Duration(seconds: 10),
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
          ),
        ) {
    // Optional dev logging
    _dio.interceptors.add(LogInterceptor(
      requestBody: true,
      responseBody: true,
    ));

    // Attach auth header automatically and handle 401s
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          if (_token != null && _token!.isNotEmpty) {
            options.headers['Authorization'] = 'Bearer ' + _token!;
          }
          return handler.next(options);
        },
        onError: (DioException e, handler) {
          // Surface 401s cleanly; a refresh flow could be added here later
          if (e.response?.statusCode == 401) {
            // keep token as-is; app layer may decide to logout
          }
          return handler.next(e);
        },
      ),
    );
  }

  /// Set or clear the bearer token used for authenticated requests.
  void setAuthToken(String? token) {
    _token = token;
    if (token == null || token.isEmpty) {
      _dio.options.headers.remove('Authorization');
    } else {
      _dio.options.headers['Authorization'] = 'Bearer $token';
    }
  }

  // Register user (our backend exposes POST /register)
  Future<User> registerUser({
    required String email,
    required String password,
    String? fullName,
  }) async {
    try {
      final Response res = await _dio.post(
        '/register',
        data: {
          'email': email,
          'password': password,
          if (fullName != null) 'full_name': fullName,
        },
      );
      if (res.data is Map<String, dynamic>) {
        return User.fromJson(res.data as Map<String, dynamic>);
      }
      throw ApiException('Unexpected response shape from /register', data: res.data);
    } on DioException catch (e) {
      throw ApiException(
        e.message ?? 'Register failed',
        statusCode: e.response?.statusCode,
        data: e.response?.data,
      );
    }
  }

  // Alternative register: POST /auth/signup (same payload, different path)
  Future<User> registerUserAuth({
    required String email,
    required String password,
    String? fullName,
  }) async {
    try {
      final Response res = await _dio.post(
        '/auth/signup',
        data: {
          'email': email,
          'password': password,
          if (fullName != null) 'full_name': fullName,
        },
      );
      if (res.data is Map<String, dynamic>) {
        return User.fromJson(res.data as Map<String, dynamic>);
      }
      throw ApiException('Unexpected response shape from /auth/signup', data: res.data);
    } on DioException catch (e) {
      throw ApiException(
        e.message ?? 'Register (auth) failed',
        statusCode: e.response?.statusCode,
        data: e.response?.data,
      );
    }
  }

  // Login: POST /auth/login returns { access_token, token_type }
  Future<String> login({
    required String email,
    required String password,
  }) async {
    try {
      final Response res = await _dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );
      final token = res.data['access_token'] as String?;
      if (token == null || token.isEmpty) {
        throw ApiException('Token not found in response', data: res.data);
      }
      // Set token for subsequent requests
      setAuthToken(token);
      return token;
    } on DioException catch (e) {
      throw ApiException(
        e.message ?? 'Login failed',
        statusCode: e.response?.statusCode,
        data: e.response?.data,
      );
    }
  }

  // Example: GET products (scaffold; endpoint to be implemented on backend)
  Future<Response<dynamic>> getProducts() async {
    try {
      final Response res = await _dio.get('/products');
      return res;
    } on DioException catch (e) {
      throw ApiException(
        e.message ?? 'Get products failed',
        statusCode: e.response?.statusCode,
        data: e.response?.data,
      );
    }
  }

  // Get current user profile using bearer token
  Future<User> me() async {
    try {
      final Response res = await _dio.get('/me');
      if (res.data is Map<String, dynamic>) {
        return User.fromJson(res.data as Map<String, dynamic>);
      }
      throw ApiException('Unexpected response shape from /me', data: res.data);
    } on DioException catch (e) {
      throw ApiException(
        e.message ?? 'Get current user failed',
        statusCode: e.response?.statusCode,
        data: e.response?.data,
      );
    }
  }
}
