# Project Blueprint

## Overview

This is a Flutter application that provides a basic authentication flow and a home screen. The application uses Firebase for authentication and Firestore for data storage. The application is built using the Model-View-Controller (MVC) architectural pattern.

## Features

- User authentication (signup, login, logout)
- User profile management (update display name, update profile picture)
- Home screen

## Project Structure

```
lib
├── app
│   ├── app.dart
│   ├── auth
│   │   ├── auth_repository.dart
│   │   └── login_screen.dart
│   └── settings
│       └── profile_screen.dart
├── features
│   ├── auth
│   │   └── presentation
│   │       ├── login_screen.dart
│   │       ├── signup_screen.dart
│   │       └── welcome_screen.dart
│   └── home
│       └── presentation
│           └── home_screen.dart
├── routes
│   └── app_router.dart
├── services
│   └── firebase_service.dart
├── splash
│   └── splash_screen.dart
├── theme
│   └── theme.dart
└── welcome
    └── welcome_screen.dart
```
