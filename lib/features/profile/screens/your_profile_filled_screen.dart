import 'package:flutter/material.dart';

class YourProfileFilledScreen extends StatelessWidget {
  const YourProfileFilledScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Set Your Profile'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const CircleAvatar(
              radius: 50,
              backgroundImage: NetworkImage('https://i.pravatar.cc/150?img=12'),
            ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: 'Andrew Ainsley',
              decoration: const InputDecoration(
                labelText: 'Full Name',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: 'andrew_ainsley',
              decoration: const InputDecoration(
                labelText: 'Username',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: '12/27/1995',
              decoration: const InputDecoration(
                labelText: 'Date of Birth',
                border: OutlineInputBorder(),
                suffixIcon: Icon(Icons.calendar_today),
              ),
            ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: 'andrew.ainsley@yourdomain.com',
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
                suffixIcon: Icon(Icons.email),
              ),
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField(
              value: 'Male',
              items: const [
                DropdownMenuItem(value: 'Male', child: Text('Male')),
                DropdownMenuItem(value: 'Female', child: Text('Female')),
              ],
              onChanged: (value) {},
              decoration: const InputDecoration(
                labelText: 'Gender',
                border: OutlineInputBorder(),
              ),
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 50),
              ),
              child: const Text('Continue'),
            ),
          ],
        ),
      ),
    );
  }
}
