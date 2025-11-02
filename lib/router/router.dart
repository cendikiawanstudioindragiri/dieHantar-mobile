import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:learn_flutter_gemini/features/payment/screens/payment_screen.dart';
import 'package:learn_flutter_gemini/features/payment/screens/payment_checked_screen.dart';
import 'package:learn_flutter_gemini/features/payment/screens/payment_add_new_card_screen.dart';
import 'package:learn_flutter_gemini/features/payment/screens/payment_add_new_card_typing_card_number_screen.dart';
import 'package:learn_flutter_gemini/features/payment/screens/payment_add_new_card_typing_cardholder_name_screen.dart';
import 'package:learn_flutter_gemini/features/payment/screens/payment_add_new_card_typing_expiry_date_screen.dart';
import 'package:learn_flutter_gemini/features/payment/screens/payment_add_new_card_typing_cvv_screen.dart';
import 'package:learn_flutter_gemini/features/payment/screens/payment_scan_qris_method_screen.dart';
import 'package:learn_flutter_gemini/features/payment/screens/payment_add_new_card_typing_cvv2_screen.dart';
import 'package:learn_flutter_gemini/features/payment/screens/payment_add_new_card_filled_screen.dart';
import 'package:learn_flutter_gemini/features/payment/screens/payment_payment_success_screen.dart';
import 'package:learn_flutter_gemini/features/payment/screens/payment_information_success_shared_my_friend_screen.dart';
import 'package:learn_flutter_gemini/features/cancel_order/screens/cancel_order_screen.dart';
import 'package:learn_flutter_gemini/features/cancel_order/screens/cancel_order_selected_screen.dart';
import 'package:learn_flutter_gemini/features/cancel_order/screens/cancel_order_other_reasons_screen.dart';
import 'package:learn_flutter_gemini/features/cancel_order/screens/cancel_order_notification_screen.dart';
import 'package:learn_flutter_gemini/features/delivery/screens/delivery_successful_screen.dart';
import 'package:learn_flutter_gemini/features/delivery/screens/order_rating_screen.dart';
import 'package:learn_flutter_gemini/features/delivery/screens/order_rating_review_screen.dart';
import 'package:learn_flutter_gemini/features/delivery/screens/driver_rating_screen.dart';
import 'package:learn_flutter_gemini/features/delivery/screens/driver_rating_review_screen.dart';
import 'package:learn_flutter_gemini/features/delivery/screens/give_thanks_screen.dart';
import 'package:learn_flutter_gemini/features/delivery/screens/give_thanks_filled_screen.dart';
import 'package:learn_flutter_gemini/features/delivery/screens/rate_your_meal_screen.dart';
import 'package:learn_flutter_gemini/features/delivery/screens/rate_your_meal_review_screen.dart';
import 'package:learn_flutter_gemini/features/delivery/screens/rate_your_meal_notification_screen.dart';
import 'package:learn_flutter_gemini/features/orders/screens/orders_screen.dart';
import 'package:learn_flutter_gemini/features/orders/screens/order_active_screen.dart';
import 'package:learn_flutter_gemini/features/orders/screens/order_completed_screen.dart';
import 'package:learn_flutter_gemini/features/orders/screens/order_cancelled_screen.dart';
import 'package:learn_flutter_gemini/features/orders/screens/order_not_found_screen.dart';
import 'package:learn_flutter_gemini/features/orders/screens/orders_active_detail_screen.dart';
import 'package:learn_flutter_gemini/features/orders/screens/orders_completed_detail_screen.dart';
import 'package:learn_flutter_gemini/features/orders/screens/orders_cancelled_detail_screen.dart';
import 'package:learn_flutter_gemini/features/liked/screens/liked_screen.dart';
import 'package:learn_flutter_gemini/features/liked/screens/liked_2_screen.dart';
import 'package:learn_flutter_gemini/features/liked/screens/liked_search_2_screen.dart';
import 'package:learn_flutter_gemini/features/liked/screens/liked_search_screen.dart';
import 'package:learn_flutter_gemini/features/liked/screens/liked_search_not_found_screen.dart';
import 'package:learn_flutter_gemini/features/liked/screens/liked_empty_screen.dart';
import 'package:learn_flutter_gemini/features/notification/screens/notification_screen.dart';
import 'package:learn_flutter_gemini/features/notification/screens/notification_2_screen.dart';
import 'package:learn_flutter_gemini/features/notification/screens/notification_search_screen.dart';
import 'package:learn_flutter_gemini/features/notification/screens/notification_search_not_found_screen.dart';
import 'package:learn_flutter_gemini/features/notification/screens/notification_search_empty_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/profile_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/profile_2_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/profile_change_user_information_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/phone_number_account_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/email_account_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/google_account_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/username_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/full_name_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/avatar_change_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/change_of_financial_sources_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/facebook_account_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/profile_logout_screen.dart';
import 'package:learn_flutter_gemini/features/profile/screens/profile_not_logged_in_yet_screen.dart';
import 'package:learn_flutter_gemini/features/messages/screens/messages_screen.dart';
import 'package:learn_flutter_gemini/features/messages/screens/message_priority_screen.dart';
import 'package:learn_flutter_gemini/features/messages/screens/messages_favorite_screen.dart';
import 'package:learn_flutter_gemini/features/invite_friends/screens/invite_friends_screen.dart';
import 'package:learn_flutter_gemini/features/help_center/screens/help_center_screen.dart';
import 'package:learn_flutter_gemini/features/help_center/screens/help_center_detail_screen.dart';
import 'package:learn_flutter_gemini/features/others/screens/term_of_service_screen.dart';
import 'package:learn_flutter_gemini/features/others/screens/privacy_policy_screen.dart';
import 'package:learn_flutter_gemini/features/others/screens/about_app_screen.dart';
import 'package:learn_flutter_gemini/features/others/screens/social_media_networks_screen.dart';
import 'package:learn_flutter_gemini/features/others/screens/donation_screen.dart';
import 'package:learn_flutter_gemini/features/others/screens/feedback_screen.dart';
import 'package:learn_flutter_gemini/more/profile_screen.dart';
import 'package:learn_flutter_gemini/cart/cart_screen.dart';

final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const PaymentScreen(),
    ),
    GoRoute(
      path: '/cart',
      builder: (context, state) => const CartScreen(),
    ),
    GoRoute(
      path: '/upload_profile',
      builder: (context, state) => const ProfileScreen(),
    ),
    GoRoute(
      path: '/payment_checked',
      builder: (context, state) => const PaymentCheckedScreen(),
    ),
    GoRoute(
      path: '/payment_add_new_card',
      builder: (context, state) => const PaymentAddNewCardScreen(),
    ),
    GoRoute(
      path: '/payment_add_new_card_typing_card_number',
      builder: (context, state) =>
          const PaymentAddNewCardTypingCardNumberScreen(),
    ),
    GoRoute(
      path: '/payment_add_new_card_typing_cardholder_name',
      builder: (context, state) =>
          const PaymentAddNewCardTypingCardholderNameScreen(),
    ),
    GoRoute(
      path: '/payment_add_new_card_typing_expiry_date',
      builder: (context, state) =>
          const PaymentAddNewCardTypingExpiryDateScreen(),
    ),
    GoRoute(
      path: '/payment_add_new_card_typing_cvv',
      builder: (context, state) => const PaymentAddNewCardTypingCvvScreen(),
    ),
    GoRoute(
      path: '/payment_scan_qris_method',
      builder: (context, state) => const PaymentScanQrisMethodScreen(),
    ),
    GoRoute(
      path: '/payment_add_new_card_typing_cvv2',
      builder: (context, state) => const PaymentAddNewCardTypingCvv2Screen(),
    ),
    GoRoute(
      path: '/payment_add_new_card_filled',
      builder: (context, state) => const PaymentAddNewCardFilledScreen(),
    ),
    GoRoute(
      path: '/payment_payment_success',
      builder: (context, state) => const PaymentPaymentSuccessScreen(),
    ),
    GoRoute(
      path: '/payment_information_success_shared_my_friend',
      builder: (context, state) =>
          const PaymentInformationSuccessSharedMyFriendScreen(),
    ),
    GoRoute(
      path: '/cancel_order',
      builder: (context, state) => const CancelOrderScreen(),
    ),
    GoRoute(
      path: '/cancel_order_selected',
      builder: (context, state) => const CancelOrderSelectedScreen(),
    ),
    GoRoute(
      path: '/cancel_order_other_reasons',
      builder: (context, state) => const CancelOrderOtherReasonsScreen(),
    ),
    GoRoute(
      path: '/cancel_order_notification',
      builder: (context, state) => const CancelOrderNotificationScreen(),
    ),
    GoRoute(
      path: '/delivery_successful',
      builder: (context, state) => const DeliverySuccessfulScreen(),
    ),
    GoRoute(
      path: '/order_rating',
      builder: (context, state) => const OrderRatingScreen(),
    ),
    GoRoute(
      path: '/order_rating_review',
      builder: (context, state) => const OrderRatingReviewScreen(),
    ),
    GoRoute(
      path: '/driver_rating',
      builder: (context, state) => const DriverRatingScreen(),
    ),
    GoRoute(
      path: '/driver_rating_review',
      builder: (context, state) => const DriverRatingReviewScreen(),
    ),
    GoRoute(
      path: '/give_thanks',
      builder: (context, state) => const GiveThanksScreen(),
    ),
    GoRoute(
      path: '/give_thanks_filled',
      builder: (context, state) => const GiveThanksFilledScreen(),
    ),
    GoRoute(
      path: '/rate_your_meal',
      builder: (context, state) => const RateYourMealScreen(),
    ),
    GoRoute(
      path: '/rate_your_meal_review',
      builder: (context, state) => const RateYourMealReviewScreen(),
    ),
    GoRoute(
      path: '/rate_your_meal_notification',
      builder: (context, state) => const RateYourMealNotificationScreen(),
    ),
    GoRoute(
      path: '/orders',
      builder: (context, state) => const OrdersScreen(),
    ),
    GoRoute(
      path: '/order_active',
      builder: (context, state) => const OrderActiveScreen(),
    ),
    GoRoute(
      path: '/order_completed',
      builder: (context, state) => const OrderCompletedScreen(),
    ),
    GoRoute(
      path: '/order_cancelled',
      builder: (context, state) => const OrderCancelledScreen(),
    ),
    GoRoute(
      path: '/order_not_found',
      builder: (context, state) => const OrderNotFoundScreen(),
    ),
    GoRoute(
      path: '/orders_active_detail',
      builder: (context, state) => const OrdersActiveDetailScreen(),
    ),
    GoRoute(
      path: '/orders_completed_detail',
      builder: (context, state) => const OrdersCompletedDetailScreen(),
    ),
    GoRoute(
      path: '/orders_cancelled_detail',
      builder: (context, state) => const OrdersCancelledDetailScreen(),
    ),
    GoRoute(
      path: '/liked',
      builder: (context, state) => const LikedScreen(),
    ),
    GoRoute(
      path: '/liked_2',
      builder: (context, state) => const Liked2Screen(),
    ),
    GoRoute(
      path: '/liked_search_2',
      builder: (context, state) => const LikedSearch2Screen(),
    ),
    GoRoute(
      path: '/liked_search',
      builder: (context, state) => const LikedSearchScreen(),
    ),
    GoRoute(
      path: '/liked_search_not_found',
      builder: (context, state) => const LikedSearchNotFoundScreen(),
    ),
    GoRoute(
      path: '/liked_empty',
      builder: (context, state) => const LikedEmptyScreen(),
    ),
    GoRoute(
      path: '/notification',
      builder: (context, state) => const NotificationScreen(),
    ),
    GoRoute(
      path: '/notification_2',
      builder: (context, state) => const Notification2Screen(),
    ),
    GoRoute(
      path: '/notification_search',
      builder: (context, state) => const NotificationSearchScreen(),
    ),
    GoRoute(
      path: '/notification_search_not_found',
      builder: (context, state) => const NotificationSearchNotFoundScreen(),
    ),
    GoRoute(
      path: '/notification_search_empty',
      builder: (context, state) => const NotificationSearchEmptyScreen(),
    ),
    GoRoute(
      path: '/profile',
      builder: (context, state) => const ProfileScreen(),
    ),
    GoRoute(
      path: '/profile_2',
      builder: (context, state) => const Profile2Screen(),
    ),
    GoRoute(
      path: '/profile_change_user_information',
      builder: (context, state) => const ProfileChangeUserInformationScreen(),
    ),
    GoRoute(
      path: '/phone_number_account',
      builder: (context, state) => const PhoneNumberAccountScreen(),
    ),
    GoRoute(
      path: '/email_account',
      builder: (context, state) => const EmailAccountScreen(),
    ),
    GoRoute(
      path: '/google_account',
      builder: (context, state) => const GoogleAccountScreen(),
    ),
    GoRoute(
      path: '/username',
      builder: (context, state) => const UsernameScreen(),
    ),
    GoRoute(
      path: '/full_name',
      builder: (context, state) => const FullNameScreen(),
    ),
    GoRoute(
      path: '/avatar_change',
      builder: (context, state) => const AvatarChangeScreen(),
    ),
    GoRoute(
      path: '/change_of_financial_sources',
      builder: (context, state) => const ChangeOfFinancialSourcesScreen(),
    ),
    GoRoute(
      path: '/facebook_account',
      builder: (context, state) => const FacebookAccountScreen(),
    ),
    GoRoute(
      path: '/profile_logout',
      builder: (context, state) => const ProfileLogoutScreen(),
    ),
    GoRoute(
      path: '/profile_not_logged_in_yet',
      builder: (context, state) => const ProfileNotLoggedInYetScreen(),
    ),
    GoRoute(
      path: '/messages',
      builder: (context, state) => const MessagesScreen(),
    ),
    GoRoute(
      path: '/message_priority',
      builder: (context, state) => const MessagePriorityScreen(),
    ),
    GoRoute(
      path: '/messages_favorite',
      builder: (context, state) => const MessagesFavoriteScreen(),
    ),
     GoRoute(
      path: '/invite_friends',
      builder: (context, state) => const InviteFriendsScreen(),
    ),
    GoRoute(
      path: '/help_center',
      builder: (context, state) => const HelpCenterScreen(),
    ),
    GoRoute(
      path: '/help_center_detail',
      builder: (context, state) => const HelpCenterDetailScreen(),
    ),
    GoRoute(
      path: '/term_of_service',
      builder: (context, state) => const TermOfServiceScreen(),
    ),
    GoRoute(
      path: '/privacy_policy',
      builder: (context, state) => const PrivacyPolicyScreen(),
    ),
    GoRoute(
      path: '/about_app',
      builder: (context, state) => const AboutAppScreen(),
    ),
    GoRoute(
      path: '/social_media_networks',
      builder: (context, state) => const SocialMediaNetworksScreen(),
    ),
    GoRoute(
      path: '/donation',
      builder: (context, state) => const DonationScreen(),
    ),
    GoRoute(
      path: '/feedback',
      builder: (context, state) => const FeedbackScreen(),
    ),
  ],
);
