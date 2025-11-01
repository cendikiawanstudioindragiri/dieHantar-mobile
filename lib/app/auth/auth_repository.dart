import 'dart:developer' as developer;
import 'package:firebase_auth/firebase_auth.dart';
import 'package:myapp/services/firebase_service.dart';

class AuthRepository {
  final AuthService _authService;

  AuthRepository(this._authService);

  User? get currentUser => _authService.currentUser;

  Stream<User?> get authStateChanges => _authService.authStateChanges;

  Future<User?> signInWithEmailAndPassword(
    String email,
    String password,
  ) async {
    try {
      final userCredential = await FirebaseAuth.instance
          .signInWithEmailAndPassword(email: email, password: password);
      return userCredential.user;
    } on FirebaseAuthException catch (e) {
      developer.log(e.message ?? 'An error occurred during sign-in.');
      return null;
    }
  }

  Future<User?> signUpWithEmailAndPassword(
    String email,
    String password,
  ) async {
    try {
      final userCredential = await FirebaseAuth.instance
          .createUserWithEmailAndPassword(email: email, password: password);
      return userCredential.user;
    } on FirebaseAuthException catch (e) {
      developer.log(e.message ?? 'An error occurred during sign-up.');
      return null;
    }
  }

  Future<void> updateUserProfilePicture(String photoURL) async {
    try {
      await currentUser?.updatePhotoURL(photoURL);
    } on FirebaseAuthException catch (e) {
      developer.log(
        e.message ?? 'An error occurred while updating the profile picture.',
      );
    }
  }

  Future<void> updateProfile({
    required String displayName,
    required String photoURL,
  }) async {
    try {
      await currentUser?.updateDisplayName(displayName);
      await currentUser?.updatePhotoURL(photoURL);
    } on FirebaseAuthException catch (e) {
      developer.log(
        e.message ?? 'An error occurred while updating the profile.',
      );
    }
  }

  Future<User?> signInWithGoogle() async {
    // Implement Google sign-in logic here.
    // This is a placeholder.
    developer.log('signInWithGoogle is not implemented yet.');
    return null;
  }

  Future<void> signOut() {
    return _authService.signOut();
  }
}
