import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:myapp/features/auth/presentation/welcome_screen.dart';
import 'package:myapp/food/screens/food_main_screen.dart';
import 'package:myapp/food/screens/restaurant_detail_screen.dart';
import 'package:myapp/food/models/restaurant_model.dart';
import 'package:myapp/ride/ride_screen.dart';
import 'package:myapp/send/send_screen.dart';
import 'package:myapp/wallet/wallet_screen.dart';
import 'package:myapp/shell/app_shell.dart';
import 'package:firebase_auth/firebase_auth.dart';

final _rootNavigatorKey = GlobalKey<NavigatorState>();
final _shellNavigatorKey = GlobalKey<NavigatorState>();

final router = GoRouter(
  navigatorKey: _rootNavigatorKey,
  initialLocation: '/',
  redirect: (BuildContext context, GoRouterState state) {
    final bool loggedIn = FirebaseAuth.instance.currentUser != null;
    final bool loggingIn = state.matchedLocation == '/';

    if (!loggedIn && !loggingIn) {
      return '/';
    }
    if (loggedIn && loggingIn) {
      return '/food';
    }
    return null;
  },
  routes: [
    GoRoute(path: '/', builder: (context, state) => const WelcomeScreen()),
    ShellRoute(
      navigatorKey: _shellNavigatorKey,
      builder: (context, state, child) {
        return AppShell(child: child);
      },
      routes: [
        GoRoute(
          path: '/food',
          builder: (context, state) => const FoodMainScreen(),
          routes: [
            GoRoute(
              path: 'restaurant',
              builder: (context, state) {
                final Restaurant restaurant = state.extra as Restaurant;
                return RestaurantDetailScreen(restaurant: restaurant);
              },
            ),
          ],
        ),
        GoRoute(path: '/ride', builder: (context, state) => RideScreen()),
        GoRoute(path: '/send', builder: (context, state) => SendScreen()),
        GoRoute(
          path: '/wallet',
          builder: (context, state) => WalletScreen(),
        ),
      ],
    ),
  ],
);
