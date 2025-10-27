import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:myapp/routes/app_router.dart';
import 'package:myapp/theme/app_theme.dart';
import 'package:myapp/features/auth/application/auth_notifier.dart';
import 'package:myapp/providers/cart_provider.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => AuthNotifier()),
        ChangeNotifierProvider(create: (context) => CartProvider()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: AppRouter.router,
      title: 'Flutter App',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system, 
      debugShowCheckedModeBanner: false,
    );
  }
}
