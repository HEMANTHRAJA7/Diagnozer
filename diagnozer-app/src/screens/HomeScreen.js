import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, SafeAreaView, StatusBar, Dimensions } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

const { width } = Dimensions.get('window');

export default function HomeScreen({ navigation }) {
  
  const handleLogout = async () => {
    await AsyncStorage.removeItem('userToken');
    navigation.replace('Login');
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={colors.background} />
      
      <View style={styles.header}>
        <Text style={typography.h1}>Select Target</Text>
        <TouchableOpacity onPress={handleLogout}>
          <Text style={{color: colors.danger, fontWeight: '600'}}>Disconnect</Text>
        </TouchableOpacity>
      </View>

      <Text style={[typography.body, styles.subtitle]}>
        Initialize diagnostic parameters by selecting the crop genome below.
      </Text>

      <View style={styles.grid}>
        <TouchableOpacity 
          style={styles.card}
          onPress={() => navigation.navigate('Scanner', { crop: 'mango' })}
          activeOpacity={0.8}
        >
          <View style={styles.cardGlow} />
          <Text style={[typography.h1, {fontSize: 40, marginBottom: 10}]}>🥭</Text>
          <Text style={typography.h2}>Mango</Text>
          <Text style={[typography.caption, {marginTop: 5, color: colors.primary}]}>Mangifera indica</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.card}
          onPress={() => navigation.navigate('Scanner', { crop: 'jackfruit' })}
          activeOpacity={0.8}
        >
          <View style={styles.cardGlow} />
          <Text style={[typography.h1, {fontSize: 40, marginBottom: 10}]}>🍈</Text>
          <Text style={typography.h2}>Jackfruit</Text>
          <Text style={[typography.caption, {marginTop: 5, color: colors.primary}]}>Artocarpus hetero.</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity 
        style={styles.chatFab}
        onPress={() => navigation.navigate('Chat')}
      >
        <Text style={typography.h3}>💬 AI Assistant</Text>
      </TouchableOpacity>
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
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 24,
    marginTop: 20
  },
  subtitle: {
    paddingHorizontal: 24,
    marginBottom: 40,
  },
  grid: {
    flex: 1,
    paddingHorizontal: 24,
    gap: 20,
  },
  card: {
    backgroundColor: colors.surface,
    borderRadius: 20,
    padding: 30,
    borderColor: colors.border,
    borderWidth: 1,
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    height: width * 0.45,
  },
  cardGlow: {
    position: 'absolute',
    width: 200,
    height: 200,
    backgroundColor: colors.primary,
    opacity: 0.03,
    borderRadius: 100,
    top: -50,
    left: -50,
  },
  chatFab: {
    position: 'absolute',
    bottom: 40,
    right: 30,
    backgroundColor: colors.surfaceLight,
    paddingHorizontal: 25,
    paddingVertical: 18,
    borderRadius: 30,
    borderColor: colors.primaryDark,
    borderWidth: 1,
    shadowColor: colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 10,
    elevation: 5,
  }
});
