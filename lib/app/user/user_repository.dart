import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:myapp/models/user_model.dart' as model;

class UserRepository {
  final FirebaseFirestore _firestore;

  UserRepository({FirebaseFirestore? firestore})
    : _firestore = firestore ?? FirebaseFirestore.instance;

  Future<void> createUser(model.User user) {
    return _firestore.collection('users').doc(user.uid).set({
      'email': user.email,
      'displayName': user.displayName,
      'photoURL': user.photoURL,
    });
  }

  Future<model.User> getUser(String uid) async {
    final snapshot = await _firestore.collection('users').doc(uid).get();
    return model.User(
      uid: snapshot.id,
      email: snapshot.data()?['email'],
      displayName: snapshot.data()?['displayName'],
      photoURL: snapshot.data()?['photoURL'],
    );
  }
}
