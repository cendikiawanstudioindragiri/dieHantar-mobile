import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

import '../services/api_service.dart';
import '../models/user_model.dart';

class SignupScreen extends StatefulWidget {
  const SignupScreen({super.key});

  @override
  State<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends State<SignupScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _fullNameController = TextEditingController();
  bool _isLoading = false;

  // NOTE: For Android emulator, consider: baseUrl: 'http://10.0.2.2:8000'
  late final ApiService _api = ApiService();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _fullNameController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);
    try {
      final String email = _emailController.text.trim();
      final String password = _passwordController.text;
      final String fullName = _fullNameController.text.trim();

      // 1) Register
      final Response res = await _api.registerUser(
        email: email,
        password: password,
        fullName: fullName.isEmpty ? null : fullName,
      );

      // Parse user (optional; backend returns the created user)
      User? createdUser;
      if (res.data is Map<String, dynamic>) {
        createdUser = User.fromJson(res.data as Map<String, dynamic>);
      }

      // 2) Login to obtain token and set header for future calls
      await _api.login(email: email, password: password);

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            createdUser != null
                ? 'Welcome, ${createdUser.fullName ?? createdUser.email}!'
                : 'Registration successful',
          ),
        ),
      );

      // TODO: Navigate to home screen
      // Navigator.of(context).pushReplacementNamed('/home');
    } on ApiException catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.message)),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Unexpected error: $e')),
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  String? _validateEmail(String? value) {
    final v = value?.trim() ?? '';
    if (v.isEmpty) return 'Email is required';
    if (!v.contains('@')) return 'Invalid email';
    return null;
  }

  String? _validatePassword(String? value) {
    final v = value ?? '';
    if (v.isEmpty) return 'Password is required';
    if (v.length < 6) return 'Minimum 6 characters';
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Sign up')),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                TextFormField(
                  controller: _fullNameController,
                  textInputAction: TextInputAction.next,
                  decoration: const InputDecoration(labelText: 'Full name (optional)'),
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  textInputAction: TextInputAction.next,
                  decoration: const InputDecoration(labelText: 'Email'),
                  validator: _validateEmail,
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: const InputDecoration(labelText: 'Password'),
                  validator: _validatePassword,
                ),
                const SizedBox(height: 24),
                ElevatedButton(
                  onPressed: _isLoading ? null : _submit,
                  child: _isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('Create account'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
