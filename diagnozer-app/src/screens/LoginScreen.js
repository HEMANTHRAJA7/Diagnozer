import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';
import api from '../services/api';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleLogin = async () => {
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await api.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      await AsyncStorage.setItem('userToken', response.data.access_token);
      navigation.replace('Home');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed Check backend connection');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={[typography.h1, { marginBottom: 10 }]}>Diagnozer</Text>
      <Text style={[typography.body, { marginBottom: 40 }]}>AI Crop Disease Detection Nexus</Text>

      {error && <Text style={styles.errorText}>{error}</Text>}

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
        onPress={handleLogin}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color={colors.background} />
        ) : (
          <Text style={typography.button}>ACCESS SYSTEMS</Text>
        )}
      </TouchableOpacity>
      
      <TouchableOpacity onPress={() => {/* Mocking register link */}}>
        <Text style={[typography.caption, { marginTop: 25, textAlign: 'center' }]}>
          Need a clearance level? <Text style={{color: colors.primary}}>Initialize Core</Text>
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    justifyContent: 'center',
    padding: 30,
  },
  input: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 8,
    padding: 16,
    marginBottom: 20,
    color: colors.text,
    fontSize: 16,
  },
  button: {
    backgroundColor: colors.primary,
    padding: 18,
    borderRadius: 8,
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
  }
});
