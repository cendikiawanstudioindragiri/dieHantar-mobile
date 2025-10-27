
import 'dart:io';

import 'package:firebase_storage/firebase_storage.dart';

class StorageRepository {
  final FirebaseStorage _firebaseStorage;

  StorageRepository({FirebaseStorage? firebaseStorage})
      : _firebaseStorage = firebaseStorage ?? FirebaseStorage.instance;

  Future<String> uploadProfilePicture(String userId, File file) async {
    final ref = _firebaseStorage.ref('users/$userId/profile.jpg');
    await ref.putFile(file);
    return ref.getDownloadURL();
  }
}
