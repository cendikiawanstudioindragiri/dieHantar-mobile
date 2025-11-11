import React, { useState, useMemo } from 'react';
import { View, Text, TextInput, Pressable, StyleSheet, Alert } from 'react-native';

// Single-file stateful LoginForm
// Two UI states (conceptual):
// - "login_empty": when username or password empty
// - "login_filled": when both fields have values
// We model these as derived state inside the same component (no separate files needed).

export default function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  // derived boolean: whether both fields are filled
  const isFilled = useMemo(() => username.trim().length > 0 && password.trim().length > 0, [username, password]);

  async function handleSubmit() {
    if (!isFilled) {
      Alert.alert('Validation', 'Please fill username and password');
      return;
    }
    setLoading(true);
    try {
      // replace with real API call or injected service
      const resp = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      if (!resp.ok) throw new Error('Login failed');
      const data = await resp.json();
      Alert.alert('Success', `Logged in as ${data?.user?.username ?? username}`);
    } catch (err) {
      Alert.alert('Error', String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Username</Text>
      <TextInput
        value={username}
        onChangeText={setUsername}
        placeholder="username"
        style={styles.input}
        autoCapitalize="none"
      />

      <Text style={styles.label}>Password</Text>
      <TextInput
        value={password}
        onChangeText={setPassword}
        placeholder="password"
        secureTextEntry
        style={styles.input}
      />

      {/* Visual difference for empty vs filled state is handled here */}
      <Pressable
        onPress={handleSubmit}
        style={[styles.button, isFilled ? styles.buttonFilled : styles.buttonEmpty]}
        disabled={loading}
      >
        <Text style={styles.buttonText}>{loading ? 'Loading...' : isFilled ? 'Log in' : 'Enter credentials'}</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 12 },
  label: { marginTop: 8, marginBottom: 4, color: '#222' },
  input: { borderWidth: 1, borderColor: '#ddd', padding: 8, borderRadius: 6 },
  button: { marginTop: 16, padding: 12, borderRadius: 8, alignItems: 'center' },
  buttonEmpty: { backgroundColor: '#eee' },
  buttonFilled: { backgroundColor: '#007AFF' },
  buttonText: { color: '#fff', fontWeight: '600' },
});
