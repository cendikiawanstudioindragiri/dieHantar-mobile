import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:myapp/providers/cart_provider.dart';
import 'package:go_router/go_router.dart';

class CheckoutScreen extends StatefulWidget {
  const CheckoutScreen({super.key});

  @override
  _CheckoutScreenState createState() => _CheckoutScreenState();
}

class _CheckoutScreenState extends State<CheckoutScreen> {
  final _formKey = GlobalKey<FormState>();
  String _address = '';

  void _placeOrder() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      
      // Tampilkan dialog konfirmasi
      showDialog(
        context: context,
        builder: (ctx) => AlertDialog(
          title: const Text('Pesanan Dikonfirmasi!'),
          content: const Text('Terima kasih, pesanan Anda sedang kami proses.'),
          actions: <Widget>[
            TextButton(
              child: const Text('OK'),
              onPressed: () {
                // Kosongkan keranjang
                Provider.of<CartProvider>(context, listen: false).clearCart();
                // Kembali ke home
                context.go('/home');
              },
            ),
          ],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final cart = Provider.of<CartProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Checkout'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Text(
              'Ringkasan Pesanan',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 10),
            _buildOrderSummary(cart),
            const SizedBox(height: 20),
            const Divider(),
            const SizedBox(height: 10),
            Text(
              'Alamat Pengiriman',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 10),
            _buildAddressForm(),
            const SizedBox(height: 30),
            _buildTotalAndOrderButton(cart),
          ],
        ),
      ),
    );
  }

  Widget _buildOrderSummary(CartProvider cart) {
    return Card(
      child: ListView.builder(
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        itemCount: cart.items.length,
        itemBuilder: (ctx, i) {
          final item = cart.items.values.toList()[i];
          return ListTile(
            title: Text(item.name),
            subtitle: Text('${item.quantity} x Rp${item.price}'),
            trailing: Text('Rp${item.price * item.quantity}'),
          );
        },
      ),
    );
  }

  Widget _buildAddressForm() {
    return Form(
      key: _formKey,
      child: TextFormField(
        decoration: const InputDecoration(
          labelText: 'Alamat Lengkap',
          border: OutlineInputBorder(),
        ),
        maxLines: 3,
        validator: (value) {
          if (value == null || value.isEmpty) {
            return 'Alamat tidak boleh kosong.';
          }
          return null;
        },
        onSaved: (value) {
          _address = value!;
        },
      ),
    );
  }

  Widget _buildTotalAndOrderButton(CartProvider cart) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text('Total Pembayaran', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            Text(
              'Rp${cart.totalAmount.toStringAsFixed(2)}',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.teal),
            ),
          ],
        ),
        const SizedBox(height: 20),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton(
            onPressed: _placeOrder,
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 15),
            ),
            child: const Text('Pesan Sekarang', style: TextStyle(fontSize: 16)),
          ),
        ),
      ],
    );
  }
}
