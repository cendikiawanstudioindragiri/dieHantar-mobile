import 'package:flutter/material.dart';

class FoodsDetailSeeMoreScreen extends StatelessWidget {
  const FoodsDetailSeeMoreScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Foods Detail See More'),
      ),
      body: const Center(
        child: Text('Foods Detail See More Screen'),
      ),
    );
  }
}
