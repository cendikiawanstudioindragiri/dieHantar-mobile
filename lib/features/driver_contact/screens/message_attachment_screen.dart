import 'package:flutter/material.dart';

class MessageAttachmentScreen extends StatelessWidget {
  const MessageAttachmentScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Message Attachment'),
      ),
      body: const Center(
        child: Text('Message Attachment Screen'),
      ),
    );
  }
}
