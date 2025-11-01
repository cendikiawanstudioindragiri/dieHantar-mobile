import 'package:flutter/material.dart';
import 'package:myapp/models/cart_item_model.dart';

class CartProvider with ChangeNotifier {
  final Map<String, CartItem> _items = {};

  Map<String, CartItem> get items => {..._items};

  int get itemCount {
    return _items.length;
  }

  double get totalAmount {
    var total = 0.0;
    _items.forEach((key, cartItem) {
      total += cartItem.price * cartItem.quantity;
    });
    return total;
  }

  void addItem(String name, int price) {
    if (_items.containsKey(name)) {
      _items.update(
        name,
        (existingCartItem) => CartItem(
          name: existingCartItem.name,
          price: existingCartItem.price,
          quantity: existingCartItem.quantity + 1,
        ),
      );
    } else {
      _items.putIfAbsent(name, () => CartItem(name: name, price: price));
    }
    notifyListeners();
  }

  void removeSingleItem(String name) {
    if (!_items.containsKey(name)) {
      return;
    }
    if (_items[name]!.quantity > 1) {
      _items.update(
        name,
        (existingCartItem) => CartItem(
          name: existingCartItem.name,
          price: existingCartItem.price,
          quantity: existingCartItem.quantity - 1,
        ),
      );
    } else {
      _items.remove(name);
    }
    notifyListeners();
  }

  void clearCart() {
    _items.clear();
    notifyListeners();
  }
}
