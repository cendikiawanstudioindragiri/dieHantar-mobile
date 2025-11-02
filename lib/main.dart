import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:learn_flutter_gemini/router/router.dart';
import 'package:learn_flutter_gemini/providers/profile_provider.dart';
import 'package:learn_flutter_gemini/providers/cart_provider.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => ProfileProvider()),
        ChangeNotifierProvider(create: (context) => CartProvider()),
      ],
      child: MaterialApp.router(
        routerConfig: router,
        title: 'deiHantar Transportasi & Makanan',
        theme: ThemeData(
          primarySwatch: Colors.deepOrange,
          visualDensity: VisualDensity.adaptivePlatformDensity,
        ),
      ),
    );
  }
}
