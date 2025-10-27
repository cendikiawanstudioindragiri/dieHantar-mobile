import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:myapp/features/auth/presentation/login_screen.dart';
import 'package:myapp/features/auth/presentation/signup_screen.dart';
import 'package:myapp/features/auth/presentation/welcome_screen.dart';
import 'package:myapp/features/home/presentation/home_screen.dart';
import 'package:myapp/app/settings/profile_screen.dart';
import 'package:myapp/app/settings/settings_screen.dart';
import 'package:myapp/order_tracking/order_tracking_screen.dart';
import 'package:myapp/notifications/notification_screen.dart';
import 'package:myapp/restaurant/restaurant_detail_screen.dart';
import 'package:myapp/cart/cart_screen.dart';

class AppRouter {
  static final GoRouter router = GoRouter(
    routes: <RouteBase>[
      GoRoute(
        path: '/',
        builder: (BuildContext context, GoRouterState state) {
          return const WelcomeScreen();
        },
      ),
      GoRoute(
        path: '/login',
        builder: (BuildContext context, GoRouterState state) {
          return LoginScreen();
        },
      ),
      GoRoute(
        path: '/signup',
        builder: (BuildContext context, GoRouterState state) {
          return SignupScreen();
        },
      ),
      GoRoute(
        path: '/home',
        builder: (BuildContext context, GoRouterState state) {
          return const HomeScreen();
        },
      ),
      GoRoute(
        path: '/profile',
        builder: (BuildContext context, GoRouterState state) {
          return const ProfileScreen();
        },
      ),
      GoRoute(
        path: '/settings',
        builder: (BuildContext context, GoRouterState state) {
          return const SettingsScreen();
        },
      ),
      GoRoute(
        path: '/track-order',
        builder: (BuildContext context, GoRouterState state) {
          final orderId = state.extra as String? ?? 'default_order_id';
          return OrderTrackingScreen(orderId: orderId);
        },
      ),
      GoRoute(
        path: '/notifications',
        builder: (BuildContext context, GoRouterState state) {
          return const NotificationScreen();
        },
      ),
      GoRoute(
        path: '/restaurant-detail',
        builder: (BuildContext context, GoRouterState state) {
          final restaurantName = state.extra as String? ?? 'Nama Restoran';
          return RestaurantDetailScreen(restaurantName: restaurantName);
        },
      ),
      GoRoute(
        path: '/cart',
        builder: (BuildContext context, GoRouterState state) {
          return const CartScreen();
        },
      ),
    ],
  );
}
