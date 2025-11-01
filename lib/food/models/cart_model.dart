import 'package:flutter/foundation.dart';
import 'package:myapp/food/models/menu_item_model.dart';

// Merepresentasikan satu item dalam keranjang belanja
class CartItem {
  final MenuItem menuItem;
  int quantity;

  CartItem({required this.menuItem, this.quantity = 1});

  double get totalPrice => menuItem.price * quantity;
}

// Mengelola state dari seluruh keranjang belanja
class CartProvider with ChangeNotifier {
  final Map<String, CartItem> _items = {};

  Map<String, CartItem> get items => {..._items};

  int get itemCount {
    return _items.length;
  }

  double get totalAmount {
    var total = 0.0;
    _items.forEach((key, cartItem) {
      total += cartItem.totalPrice;
    });
    return total;
  }

  void addItem(MenuItem menuItem) {
    if (_items.containsKey(menuItem.id)) {
      // Hanya tingkatkan kuantitas
      _items.update(
        menuItem.id,
        (existingCartItem) => CartItem(
          menuItem: existingCartItem.menuItem,
          quantity: existingCartItem.quantity + 1,
        ),
      );
    } else {
      // Tambahkan item baru
      _items.putIfAbsent(menuItem.id, () => CartItem(menuItem: menuItem));
    }
    notifyListeners();
  }

  void removeSingleItem(String menuItemId) {
    if (!_items.containsKey(menuItemId)) return;

    if (_items[menuItemId]!.quantity > 1) {
      _items.update(
        menuItemId,
        (existingCartItem) => CartItem(
          menuItem: existingCartItem.menuItem,
          quantity: existingCartItem.quantity - 1,
        ),
      );
    } else {
      _items.remove(menuItemId);
    }
    notifyListeners();
  }

  void removeItem(String menuItemId) {
    _items.remove(menuItemId);
    notifyListeners();
  }

  void clear() {
    _items.clear();
    notifyListeners();
  }
}
