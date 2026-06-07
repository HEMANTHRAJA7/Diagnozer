import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator, SafeAreaView, StatusBar } from 'react-native';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';
import api from '../services/api';

export default function RegisterScreen({ navigation }) {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleRegister = async () => {
    if (!fullName.trim() || !email.trim() || !password.trim()) {
      setError('Please fill in all security parameters.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      await api.post('/auth/register', {
        email: email.trim(),
        password: password.trim(),
        full_name: fullName.trim()
      });
      
      setSuccess(true);
      setTimeout(() => {
        navigation.navigate('Login');
      }, 1500);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Account initialization failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={colors.background} />
      
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={{ color: colors.primary, fontWeight: '600', fontSize: 16 }}>← Back</Text>
        </TouchableOpacity>
        <Text style={typography.h2}>Register Core</Text>
        <View style={{ width: 50 }} />
      </View>

      <View style={styles.content}>
        <Text style={[typography.h1, { marginBottom: 10 }]}>Initialize Account</Text>
        <Text style={[typography.body, { marginBottom: 40 }]}>Provide credentials to request clearance level.</Text>

        {error && <Text style={styles.errorText}>{error}</Text>}
        {success && <Text style={styles.successText}>Core Initialized! Redirecting to login...</Text>}

        <TextInput
          style={styles.input}
          placeholder="Full Name"
          placeholderTextColor={colors.textSecondary}
          value={fullName}
          onChangeText={setFullName}
          autoCapitalize="words"
        />

        <TextInput
          style={styles.input}
          placeholder="User Email"
          placeholderTextColor={colors.textSecondary}
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
        />
        
        <TextInput
          style={styles.input}
          placeholder="Security Key (Password)"
          placeholderTextColor={colors.textSecondary}
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <TouchableOpacity 
          style={styles.button} 
          onPress={handleRegister}
          disabled={loading || success}
        >
          {loading ? (
            <ActivityIndicator color={colors.background} />
          ) : (
            <Text style={typography.button}>CREATE CREDENTIALS</Text>
          )}
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 24,
    borderBottomWidth: 1,
    borderColor: colors.border,
    marginTop: 10
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    padding: 30,
  },
  input: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    color: colors.text,
    fontSize: 16,
  },
  button: {
    backgroundColor: colors.primary,
    padding: 18,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 10,
    shadowColor: colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 8,
  },
  errorText: {
    color: colors.danger,
    marginBottom: 20,
    textAlign: 'center',
  },
  successText: {
    color: colors.primary,
    marginBottom: 20,
    textAlign: 'center',
    fontWeight: '600'
  }
});
