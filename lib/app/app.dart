import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:myapp/app/auth/auth_repository.dart';
import 'package:myapp/features/auth/presentation/login_screen.dart';
import 'package:myapp/features/auth/presentation/signup_screen.dart';
import 'package:myapp/features/auth/presentation/welcome_screen.dart';
import 'package:myapp/features/home/presentation/home_screen.dart';
import 'package:myapp/services/firebase_service.dart';
import 'package:myapp/splash/splash_screen.dart';
import 'package:myapp/theme/theme.dart';
import 'package:provider/provider.dart';
import 'package:myapp/auth/auth_service.dart';

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  late final GoRouter _router;
  late final AuthService _authService;

  @override
  void initState() {
    super.initState();
    _authService = AuthService();
    _router = GoRouter(
      initialLocation: '/',
      refreshListenable: _authService,
      redirect: (BuildContext context, GoRouterState state) {
        final bool loggedIn = _authService.currentUser != null;
        final bool loggingIn =
            state.matchedLocation == '/login' ||
            state.matchedLocation == '/signup' ||
            state.matchedLocation == '/welcome';

        if (!loggedIn) {
          return loggingIn ? null : '/welcome';
        }

        if (loggingIn) {
          return '/home';
        }

        return null;
      },
      routes: <RouteBase>[
        GoRoute(
          path: '/',
          builder: (BuildContext context, GoRouterState state) {
            return const SplashScreen();
          },
        ),
        GoRoute(
          path: '/welcome',
          builder: (BuildContext context, GoRouterState state) {
            return const WelcomeScreen();
          },
        ),
        GoRoute(
          path: '/login',
          builder: (BuildContext context, GoRouterState state) {
            return const LoginScreen();
          },
        ),
        GoRoute(
          path: '/signup',
          builder: (BuildContext context, GoRouterState state) {
            return const SignupScreen();
          },
        ),
        GoRoute(
          path: '/home',
          builder: (BuildContext context, GoRouterState state) {
            return const HomeScreen();
          },
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: _authService),
        Provider<OrderService>(create: (_) => OrderService()),
        Provider<DataService>(create: (_) => DataService()),
        ProxyProvider<AuthService, AuthRepository>(
          update: (context, authService, _) => AuthRepository(authService),
        ),
        ChangeNotifierProvider(create: (context) => ThemeProvider()),
        ChangeNotifierProvider(create: (_) => AuthService()), // Added this line
      ],
      child: Consumer<ThemeProvider>(
        builder: (context, themeProvider, child) {
          return MaterialApp.router(
            title: 'Cendikiawan Studios',
            theme: lightTheme,
            darkTheme: darkTheme,
            themeMode: themeProvider.themeMode,
            routerConfig: _router,
            debugShowCheckedModeBanner: false,
          );
        },
      ),
    );
  }
}
