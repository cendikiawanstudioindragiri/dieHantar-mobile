import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/cart_provider.dart';
import '../../models/cart_item_model.dart';

class CartItemWidget extends StatelessWidget {
  final String productId;
  final CartItem cartItem;

  const CartItemWidget({super.key, required this.productId, required this.cartItem});

  @override
  Widget build(BuildContext context) {
    final cart = Provider.of<CartProvider>(context, listen: false);

    return Dismissible(
      key: ValueKey(cartItem.id),
      direction: DismissDirection.endToStart,
      onDismissed: (direction) {
        cart.removeItem(productId);
      },
      background: Container(
        color: Theme.of(context).colorScheme.error,
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 20),
        margin: const EdgeInsets.symmetric(horizontal: 15, vertical: 4),
        child: const Icon(
          Icons.delete,
          color: Colors.white,
          size: 40,
        ),
      ),
      child: Card(
        margin: const EdgeInsets.symmetric(horizontal: 15, vertical: 4),
        child: Padding(
          padding: const EdgeInsets.all(8),
          child: ListTile(
            leading: CircleAvatar(
              backgroundImage: NetworkImage(cartItem.imageUrl),
            ),
            title: Text(cartItem.name),
            subtitle: Text('Total: Rp${(cartItem.price * cartItem.quantity).toStringAsFixed(0)}'),
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: <Widget>[
                IconButton(
                  icon: const Icon(Icons.remove),
                  onPressed: () {
                    cart.removeSingleItem(productId);
                  },
                ),
                Text('${cartItem.quantity}x'),
                IconButton(
                  icon: const Icon(Icons.add),
                  onPressed: () {
                    cart.addItem(productId, cartItem.name, cartItem.price, cartItem.imageUrl);
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
