import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';// Di dalam file service atau repository Flutter Anda
import 'package:http/http.dart' as http;
import 'dart:convert';

// Definisikan sebuah model untuk notifikasi agar kode lebih rapi dan aman
class Notification {
  final String id;
  final String title;
  final String body;

  Notification({required this.id, required this.title, required this.body});

  factory Notification.fromJson(Map<String, dynamic> json) {
    return Notification(
      id: json['id'],
      title: json['title'],
      body: json['body'],
    );
  }
}

// Fungsi untuk mengambil data dari backend
Future<List<Notification>> fetchNotifications() async {
  // Ganti URL ini dengan URL Cloud Run backend Anda setelah di-deploy
  final response = await http.get(Uri.parse('https://your-backend-url.com/notifications'));

  if (response.statusCode == 200) {
    // Jika server mengembalikan respons OK (200),
    // maka parse JSON.
    List<dynamic> body = jsonDecode(response.body);
    List<Notification> notifications = body.map(
      (dynamic item) => Notification.fromJson(item),
    ).toList();
    return notifications;
  } else {
    // Jika respons tidak OK, lempar exception.
    throw Exception('Failed to load notifications');
  }
}

import 'package:gemini_flutter_app/features/login/screens/screens.dart';
import 'package:gemini_flutter_app/features/otp/screens/screens.dart';
import 'package:gemini_flutter_app/features/profile/screens/screens.dart';
import 'package:gemini_flutter_app/features/touch_id/screens/screens.dart';
import 'package:gemini_flutter_app/features/pin_security/screens/screens.dart';
import 'package:gemini_flutter_app/features/home/screens/screens.dart';
import 'package:gemini_flutter_app/features/location/screens/screens.dart';
import 'package:gemini_flutter_app/features/foods/screens/screens.dart';
import 'package:gemini_flutter_app/features/drinks/screens/screens.dart';
import 'package:gemini_flutter_app/features/services/screens/screens.dart';
import 'package:gemini_flutter_app/features/my_basket/screens/screens.dart';
import 'package:gemini_flutter_app/features/order_tracking/screens/screens.dart';
import 'package:gemini_flutter_app/features/driver_contact/screens/screens.dart';

final GoRouter router = GoRouter(
  routes: <RouteBase>[
    GoRoute(
      path: '/',
      builder: (BuildContext context, GoRouterState state) {
        return const LoadingStartScreen();
      },
    ),
    GoRoute(
      path: '/loading-start',
      builder: (BuildContext context, GoRouterState state) {
        return const LoadingStartScreen();
      },
    ),
    GoRoute(
      path: '/loading-middle',
      builder: (BuildContext context, GoRouterState state) {
        return const LoadingMiddleScreen();
      },
    ),
    GoRoute(
      path: '/loading-done',
      builder: (BuildContext context, GoRouterState state) {
        return const LoadingDoneScreen();
      },
    ),
    GoRoute(
      path: '/welcome',
      builder: (BuildContext context, GoRouterState state) {
        return const WelcomeScreen();
      },
    ),
    GoRoute(
      path: '/introduce-step1',
      builder: (BuildContext context, GoRouterState state) {
        return const IntroduceStep1Screen();
      },
    ),
    GoRoute(
      path: '/introduce-step2',
      builder: (BuildContext context, GoRouterState state) {
        return const IntroduceStep2Screen();
      },
    ),
    GoRoute(
      path: '/introduce-step3',
      builder: (BuildContext context, GoRouterState state) {
        return const IntroduceStep3Screen();
      },
    ),
    GoRoute(
      path: '/introduce-step4',
      builder: (BuildContext context, GoRouterState state) {
        return const IntroduceStep4Screen();
      },
    ),
    GoRoute(
      path: '/login-empty',
      builder: (BuildContext context, GoRouterState state) {
        return const LoginEmptyScreen();
      },
    ),
    GoRoute(
      path: '/login-typing',
      builder: (BuildContext context, GoRouterState state) {
        return const LoginTypingScreen();
      },
    ),
    GoRoute(
      path: '/login-filled',
      builder: (BuildContext context, GoRouterState state) {
        return const LoginFilledScreen();
      },
    ),
    GoRoute(
      path: '/signup-empty',
      builder: (BuildContext context, GoRouterState state) {
        return const SignupEmptyScreen();
      },
    ),
    GoRoute(
      path: '/signup-typing1',
      builder: (BuildContext context, GoRouterState state) {
        return const SignupTyping1Screen();
      },
    ),
    GoRoute(
      path: '/signup-typing2',
      builder: (BuildContext context, GoRouterState state) {
        return const SignupTyping2Screen();
      },
    ),
    GoRoute(
      path: '/signup-typing3',
      builder: (BuildContext context, GoRouterState state) {
        return const SignupTyping3Screen();
      },
    ),
    GoRoute(
      path: '/signup-typing',
      builder: (BuildContext context, GoRouterState state) {
        return const SignupTypingScreen();
      },
    ),
    GoRoute(
      path: '/signup-filled',
      builder: (BuildContext context, GoRouterState state) {
        return const SignupFilledScreen();
      },
    ),
    GoRoute(
      path: '/forgot-password-empty',
      builder: (BuildContext context, GoRouterState state) {
        return const ForgotPasswordEmptyScreen();
      },
    ),
    GoRoute(
      path: '/verification-empty',
      builder: (BuildContext context, GoRouterState state) {
        return const VerificationEmptyScreen();
      },
    ),
    GoRoute(
      path: '/verification-typing',
      builder: (BuildContext context, GoRouterState state) {
        return const VerificationTypingScreen();
      },
    ),
    GoRoute(
      path: '/verification-filled',
      builder: (BuildContext context, GoRouterState state) {
        return const VerificationFilledScreen();
      },
    ),
    GoRoute(
      path: '/verification-error',
      builder: (BuildContext context, GoRouterState state) {
        return const VerificationErrorScreen();
      },
    ),
    GoRoute(
      path: '/verification-resend-code',
      builder: (BuildContext context, GoRouterState state) {
        return const VerificationResendCodeScreen();
      },
    ),
    GoRoute(
      path: '/verification-resend-code-notification',
      builder: (BuildContext context, GoRouterState state) {
        return const VerificationResendCodeNotificationScreen();
      },
    ),
    GoRoute(
      path: '/your-profile',
      builder: (BuildContext context, GoRouterState state) {
        return const YourProfileScreen();
      },
    ),
    GoRoute(
      path: '/your-profile-scroll-up',
      builder: (BuildContext context, GoRouterState state) {
        return const YourProfileScrollUpScreen();
      },
    ),
    GoRoute(
      path: '/your-profile-filled',
      builder: (BuildContext context, GoRouterState state) {
        return const YourProfileFilledScreen();
      },
    ),
    GoRoute(
      path: '/your-profile-filled-scroll-up',
      builder: (BuildContext context, GoRouterState state) {
        return const YourProfileFilledScrollUpScreen();
      },
    ),
    GoRoute(
      path: '/setting-touch-id',
      builder: (BuildContext context, GoRouterState state) {
        return const SettingTouchIdScreen();
      },
    ),
    GoRoute(
      path: '/setting-touch-id-scanning',
      builder: (BuildContext context, GoRouterState state) {
        return const SettingTouchIdScanningScreen();
      },
    ),
    GoRoute(
      path: '/setting-touch-id-done',
      builder: (BuildContext context, GoRouterState state) {
        return const SettingTouchIdDoneScreen();
      },
    ),
    GoRoute(
      path: '/setting-pin-security',
      builder: (BuildContext context, GoRouterState state) {
        return const SettingPinSecurityScreen();
      },
    ),
    GoRoute(
      path: '/setting-pin-security-scanning',
      builder: (BuildContext context, GoRouterState state) {
        return const SettingPinSecurityScanningScreen();
      },
    ),
    GoRoute(
      path: '/setting-pin-security-done',
      builder: (BuildContext context, GoRouterState state) {
        return const SettingPinSecurityDoneScreen();
      },
    ),
    GoRoute(
      path: '/home',
      builder: (BuildContext context, GoRouterState state) {
        return const HomeScreen();
      },
    ),
    GoRoute(
      path: '/home-full-user-info',
      builder: (BuildContext context, GoRouterState state) {
        return const HomeFullUserInfoScreen();
      },
    ),
    GoRoute(
      path: '/my-location',
      builder: (BuildContext context, GoRouterState state) {
        return const MyLocationScreen();
      },
    ),
    GoRoute(
      path: '/my-location-add-new-location',
      builder: (BuildContext context, GoRouterState state) {
        return const MyLocationAddNewLocationScreen();
      },
    ),
    GoRoute(
      path: '/my-location-added-new-location',
      builder: (BuildContext context, GoRouterState state) {
        return const MyLocationAddedNewLocationScreen();
      },
    ),
    GoRoute(
      path: '/my-location-added-new-location-has-driver-icon',
      builder: (BuildContext context, GoRouterState state) {
        return const MyLocationAddedNewLocationHasDriverIconScreen();
      },
    ),
    GoRoute(
      path: '/my-locations',
      builder: (BuildContext context, GoRouterState state) {
        return const MyLocationsScreen();
      },
    ),
    GoRoute(
      path: '/my-locations-favorite',
      builder: (BuildContext context, GoRouterState state) {
        return const MyLocationsFavoriteScreen();
      },
    ),
    GoRoute(
      path: '/foods-categories',
      builder: (BuildContext context, GoRouterState state) {
        return const FoodsCategoriesScreen();
      },
    ),
    GoRoute(
      path: '/drinks-categories',
      builder: (BuildContext context, GoRouterState state) {
        return const DrinksCategoriesScreen();
      },
    ),
    GoRoute(
      path: '/services-categories',
      builder: (BuildContext context, GoRouterState state) {
        return const ServicesCategoriesScreen();
      },
    ),
    GoRoute(
      path: '/foods',
      builder: (BuildContext context, GoRouterState state) {
        return const FoodsScreen();
      },
    ),
    GoRoute(
      path: '/foods-search',
      builder: (BuildContext context, GoRouterState state) {
        return const FoodsSearchScreen();
      },
    ),
    GoRoute(
      path: '/foods-search-not-found',
      builder: (BuildContext context, GoRouterState state) {
        return const FoodsSearchNotFoundScreen();
      },
    ),
    GoRoute(
      path: '/foods-detail',
      builder: (BuildContext context, GoRouterState state) {
        return const FoodsDetailScreen();
      },
    ),
    GoRoute(
      path: '/foods-detail-see-more',
      builder: (BuildContext context, GoRouterState state) {
        return const FoodsDetailSeeMoreScreen();
      },
    ),
    GoRoute(
      path: '/foods-detail-select',
      builder: (BuildContext context, GoRouterState state) {
        return const FoodsDetailSelectScreen();
      },
    ),
    GoRoute(
      path: '/foods-detail-select2',
      builder: (BuildContext context, GoRouterState state) {
        return const FoodsDetailSelect2Screen();
      },
    ),
    GoRoute(
      path: '/foods-add-basket',
      builder: (BuildContext context, GoRouterState state) {
        return const FoodsAddBasketScreen();
      },
    ),
    GoRoute(
      path: '/foods-detail-see-all-review',
      builder: (BuildContext context, GoRouterState state) {
        return const FoodsDetailSeeAllReviewScreen();
      },
    ),
    GoRoute(
      path: '/foods-detail-share-friends',
      builder: (BuildContext context, GoRouterState state) {
        return const FoodsDetailShareFriendsScreen();
      },
    ),
    GoRoute(
      path: '/drinks',
      builder: (BuildContext context, GoRouterState state) {
        return const DrinksScreen();
      },
    ),
    GoRoute(
      path: '/drinks-search',
      builder: (BuildContext context, GoRouterState state) {
        return const DrinksSearchScreen();
      },
    ),
    GoRoute(
      path: '/drinks-search-not-found',
      builder: (BuildContext context, GoRouterState state) {
        return const DrinksSearchNotFoundScreen();
      },
    ),
    GoRoute(
      path: '/drinks-detail',
      builder: (BuildContext context, GoRouterState state) {
        return const DrinksDetailScreen();
      },
    ),
    GoRoute(
      path: '/drinks-detail-see-more',
      builder: (BuildContext context, GoRouterState state) {
        return const DrinksDetailSeeMoreScreen();
      },
    ),
    GoRoute(
      path: '/drinks-detail-select',
      builder: (BuildContext context, GoRouterState state) {
        return const DrinksDetailSelectScreen();
      },
    ),
    GoRoute(
      path: '/drinks-detail-select2',
      builder: (BuildContext context, GoRouterState state) {
        return const DrinksDetailSelect2Screen();
      },
    ),
    GoRoute(
      path: '/drinks-add-basket',
      builder: (BuildContext context, GoRouterState state) {
        return const DrinksAddBasketScreen();
      },
    ),
    GoRoute(
      path: '/drinks-detail-see-all-review',
      builder: (BuildContext context, GoRouterState state) {
        return const DrinksDetailSeeAllReviewScreen();
      },
    ),
    GoRoute(
      path: '/drinks-detail-share-friends',
      builder: (BuildContext context, GoRouterState state) {
        return const DrinksDetailShareFriendsScreen();
      },
    ),
    GoRoute(
      path: '/services',
      builder: (BuildContext context, GoRouterState state) {
        return const ServicesScreen();
      },
    ),
    GoRoute(
      path: '/services-search',
      builder: (BuildContext context, GoRouterState state) {
        return const ServicesSearchScreen();
      },
    ),
    GoRoute(
      path: '/services-search-not-found',
      builder: (BuildContext context, GoRouterState state) {
        return const ServicesSearchNotFoundScreen();
      },
    ),
    GoRoute(
      path: '/services-detail',
      builder: (BuildContext context, GoRouterState state) {
        return const ServicesDetailScreen();
      },
    ),
    GoRoute(
      path: '/services-detail-see-more',
      builder: (BuildContext context, GoRouterState state) {
        return const ServicesDetailSeeMoreScreen();
      },
    ),
    GoRoute(
      path: '/services-detail-select',
      builder: (BuildContext context, GoRouterState state) {
        return const ServicesDetailSelectScreen();
      },
    ),
    GoRoute(
      path: '/services-detail-select2',
      builder: (BuildContext context, GoRouterState state) {
        return const ServicesDetailSelect2Screen();
      },
    ),
    GoRoute(
      path: '/services-add-basket',
      builder: (BuildContext context, GoRouterState state) {
        return const ServicesAddBasketScreen();
      },
    ),
    GoRoute(
      path: '/services-detail-see-all-review',
      builder: (BuildContext context, GoRouterState state) {
        return const ServicesDetailSeeAllReviewScreen();
      },
    ),
    GoRoute(
      path: '/services-detail-share-friends',
      builder: (BuildContext context, GoRouterState state) {
        return const ServicesDetailShareFriendsScreen();
      },
    ),
    GoRoute(
      path: '/my-basket',
      builder: (BuildContext context, GoRouterState state) {
        return const MyBasketScreen();
      },
    ),
    GoRoute(
      path: '/my-basket2',
      builder: (BuildContext context, GoRouterState state) {
        return const MyBasket2Screen();
      },
    ),
    GoRoute(
      path: '/my-basket-full-info',
      builder: (BuildContext context, GoRouterState state) {
        return const MyBasketFullInfoScreen();
      },
    ),
    GoRoute(
      path: '/order-tracking',
      builder: (BuildContext context, GoRouterState state) {
        return const OrderTrackingScreen();
      },
    ),
    GoRoute(
      path: '/order-tracking-step1',
      builder: (BuildContext context, GoRouterState state) {
        return const OrderTrackingStep1Screen();
      },
    ),
    GoRoute(
      path: '/order-tracking-step2',
      builder: (BuildContext context, GoRouterState state) {
        return const OrderTrackingStep2Screen();
      },
    ),
    GoRoute(
      path: '/order-tracking-step3',
      builder: (BuildContext context, GoRouterState state) {
        return const OrderTrackingStep3Screen();
      },
    ),
    GoRoute(
      path: '/order-tracking-step4',
      builder: (BuildContext context, GoRouterState state) {
        return const OrderTrackingStep4Screen();
      },
    ),
    GoRoute(
      path: '/driver-information',
      builder: (BuildContext context, GoRouterState state) {
        return const DriverInformationScreen();
      },
    ),
    GoRoute(
      path: '/message',
      builder: (BuildContext context, GoRouterState state) {
        return const MessageScreen();
      },
    ),
    GoRoute(
      path: '/message-attachment',
      builder: (BuildContext context, GoRouterState state) {
        return const MessageAttachmentScreen();
      },
    ),
    GoRoute(
      path: '/message2',
      builder: (BuildContext context, GoRouterState state) {
        return const Message2Screen();
      },
    ),
    GoRoute(
      path: '/call',
      builder: (BuildContext context, GoRouterState state) {
        return const CallScreen();
      },
    ),
    GoRoute(
      path: '/calling',
      builder: (BuildContext context, GoRouterState state) {
        return const CallingScreen();
      },
    ),
    GoRoute(
      path: '/report-account-and-bug',
      builder: (BuildContext context, GoRouterState state) {
        return const ReportAccountAndBugScreen();
      },
    ),
  ],
);
