import 'package:flutter/material.dart';
import 'package:pinput/pinput.dart';

class VerificationResendCodeScreen extends StatefulWidget {
  const VerificationResendCodeScreen({super.key});

  @override
  State<VerificationResendCodeScreen> createState() => _VerificationResendCodeScreenState();
}

class _VerificationResendCodeScreenState extends State<VerificationResendCodeScreen> {
  bool _isCodeResent = false;

  void _resendCode() {
    setState(() {
      _isCodeResent = true;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Code Resent!'),
        duration: Duration(seconds: 2),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('OTP Verification'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              'Enter the OTP sent to your mobile number',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 24),
            Pinput(
              length: 6,
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 50),
              ),
              child: const Text('Verify'),
            ),
            const SizedBox(height: 12),
            TextButton(
              onPressed: _resendCode,
              child: const Text('Resend Code'),
            ),
          ],
        ),
      ),
    );
  }
}
