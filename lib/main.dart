import 'package:flutter/material.dart';
import 'package:learn_flutter_gemini/router/router.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: router,
      title: 'Flutter Payment App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
    );
  }
}
