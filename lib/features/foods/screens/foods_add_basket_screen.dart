import 'package:flutter/material.dart';

class FoodsAddBasketScreen extends StatelessWidget {
  const FoodsAddBasketScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Foods Add Basket'),
      ),
      body: const Center(
        child: Text('Foods Add Basket Screen'),
      ),
    );
  }
}
