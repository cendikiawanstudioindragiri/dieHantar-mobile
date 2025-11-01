# dieHantar Super App Blueprint

## 1. Overview

**dieHantar** is evolving from a food delivery service into a "super app" designed to be an indispensable part of a user's daily life. The goal is to create an integrated ecosystem of on-demand services, starting with food delivery and expanding into transportation, logistics, and digital payments, all accessible through a single, intuitive mobile application.

This blueprint outlines the current features, the planned expansion, and the technical roadmap for implementation.

## 2. Current Implemented Features (Food Delivery)

-   **User Authentication:** Secure signup, login, and logout.
-   **Restaurant Browsing:** A home screen to discover and view restaurants.
-   **Menu & Ordering:** Detailed restaurant screens with menus to add items to a cart.
-   **Shopping Cart:** A fully functional cart to review and manage items.
-   **Checkout Process:** A simulated order placement and checkout flow.
-   **Reviews & Ratings (Static):** UI for submitting and viewing reviews, currently using static data.
-   **Notifications (Static):** A notification screen displaying hardcoded updates.

## 3. Planned Super App Expansion

### Core Services
-   **`dieHantar Food`:** (Existing) The core food delivery service.
-   **`dieHantar Ride`:** A ride-hailing service for ordering motorcycle taxis (Ojek) and cars.
-   **`dieHantar Send`:** An instant courier service for package delivery.

### Core Features
-   **`dieHantar Wallet`:** An integrated e-wallet for seamless, one-tap payments across all services. Users can top up their balance and view transaction history.
-   **Live Driver Tracking:** A real-time map interface to track the driver's location for food orders, rides, and package deliveries.
-   **In-App Chat:** A secure chat feature for direct communication between users and drivers/riders.
-   **Dynamic Notification System:** A backend-driven system to push real-time updates (order status, driver location, promos) to users.
-   **Promo & Voucher System:** A flexible backend to manage promotional campaigns, discounts, and loyalty rewards.

## 4. Current Development Plan

**Objective:** Build the foundational backend services required for dynamic features.

1.  **Implement Reviews & Ratings API:**
    *   Create a `POST /reviews` endpoint in `functions/main.py` to allow users to submit a new review for an order.
    *   Create a `GET /reviews?restaurantId=<id>` endpoint to fetch all reviews for a specific restaurant.
    *   Connect the Flutter frontend (`rating_screen.dart` and `reviews_list_screen.dart`) to these new APIs.
    *   Store review data in Firestore.

2.  **Implement Dynamic Notifications API:**
    *   Create a `GET /notifications?userId=<id>` endpoint to fetch a user's notifications.
    *   Modify the `notification_screen.dart` to fetch data from this API instead of using a static list.
    *   Integrate with Firebase Cloud Messaging (FCM) to push real-time status updates in the future.

---
*This blueprint will be updated as new features are implemented.*
