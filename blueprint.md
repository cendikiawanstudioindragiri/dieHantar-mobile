# Project Blueprint

## Overview

This is a Flutter application that provides a food delivery-like experience. It includes user authentication, a home screen to browse restaurants, a shopping cart, and a checkout process. The application uses Firebase for authentication.

## Features

- User authentication (signup, login, logout)
- User profile management (update display name, update profile picture)
- Home screen with restaurant listings
- Restaurant detail screen with menu items
- Shopping Cart
    - Add items to cart
    - View items in cart
    - See total price
- Checkout Process
    - Enter shipping address
    - Confirm order
    - Simulated order placement
- **Reviews and Ratings**
    - Users can give a star rating and a written review after an order is complete.
    - Users can view a list of all reviews for a specific restaurant.

## Project Structure

```
lib
├── app
│   ├── settings
│   │   ├── profile_screen.dart
│   │   └── settings_screen.dart
├── cart
│   └── cart_screen.dart
├── checkout
│   └── checkout_screen.dart
├── features
│   ├── auth
│   │   └── presentation
│   │       ├── login_screen.dart
│   │       ├── signup_screen.dart
│   │       └── welcome_screen.dart
│   └── home
│       └── presentation
│           └── home_screen.dart
├── models
│   ├── cart_item_model.dart
│   └── review_model.dart
├── notifications
│   └── notification_screen.dart
├── order_tracking
│   └── order_tracking_screen.dart
├── providers
│   ├── cart_provider.dart
│   └── review_provider.dart
├── rating
│   ├── rating_screen.dart
│   └── reviews_list_screen.dart
├── restaurant
│   └── restaurant_detail_screen.dart
├── routes
│   └── app_router.dart
├── services
│   └── firebase_service.dart
├── splash
│   └── splash_screen.dart
└── welcome
    └── welcome_screen.dart
```
