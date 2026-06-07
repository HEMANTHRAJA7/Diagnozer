import React from 'react';
import { View, Text, StyleSheet, Image, ScrollView, TouchableOpacity, SafeAreaView, StatusBar } from 'react-native';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

export default function ResultScreen({ route, navigation }) {
  const { resultData, crop } = route.params;

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={colors.background} />
      
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.navigate('Home')}>
          <Text style={{ color: colors.primary, fontWeight: '600', fontSize: 16 }}>← Back</Text>
        </TouchableOpacity>
        <Text style={typography.h2}>AI Diagnosis</Text>
        <View style={{ width: 50 }} />
      </View>

      <ScrollView contentContainerStyle={{alignItems: 'center', padding: 20}}>
        <View style={styles.card}>
          <Image 
            source={{ uri: resultData.heatmapUrl || 'https://via.placeholder.com/224' }} 
            style={styles.heatmap} 
            resizeMode="cover"
          />
          
          <View style={styles.analysisBox}>
            <Text style={typography.caption}>CONFIDENCE MATCH</Text>
            <Text style={[typography.h2, { color: colors.primary }]}>
              {(resultData.confidence * 100).toFixed(1)}%
            </Text>
          </View>

          <View style={styles.analysisBox}>
            <Text style={typography.caption}>DETECTED PATHOGEN</Text>
            <Text style={typography.h3}>
              {resultData.predictedClass.replace(/_/g, ' ')}
            </Text>
          </View>

          {resultData.imageType && (
            <View style={[styles.analysisBox, { borderBottomWidth: 0 }]}>
              <Text style={typography.caption}>IMAGE TARGET</Text>
              <Text style={typography.body}>{resultData.imageType}</Text>
            </View>
          )}
        </View>

        <Text style={[typography.body, { textAlign: 'center', marginTop: 20, marginBottom: 30 }]}>
          {resultData.explanation}
        </Text>

        <TouchableOpacity 
          style={styles.button}
          onPress={() => navigation.navigate('Chat')}
        >
          <Text style={typography.button}>ASK CHATBOT FOR TREATMENT</Text>
        </TouchableOpacity>
      </ScrollView>
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
  card: {
    backgroundColor: colors.surface,
    borderRadius: 20,
    width: '100%',
    marginTop: 20,
    borderColor: colors.border,
    borderWidth: 1,
    overflow: 'hidden'
  },
  heatmap: {
    width: '100%',
    height: 300,
    borderBottomWidth: 1,
    borderColor: colors.border
  },
  analysisBox: {
    padding: 20,
    borderBottomWidth: 1,
    borderColor: colors.border,
  },
  button: {
    backgroundColor: colors.primary,
    padding: 18,
    borderRadius: 12,
    width: '100%',
    alignItems: 'center',
    shadowColor: colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 8,
    marginBottom: 40
  }
});

