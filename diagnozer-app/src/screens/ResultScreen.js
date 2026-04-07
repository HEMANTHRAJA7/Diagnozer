import React from 'react';
import { View, Text, StyleSheet, Image, ScrollView, TouchableOpacity } from 'react-native';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

export default function ResultScreen({ route, navigation }) {
  const { resultData, crop } = route.params;

  return (
    <ScrollView style={styles.container} contentContainerStyle={{alignItems: 'center', padding: 20}}>
      <Text style={[typography.h1, { marginTop: 40 }]}>AI Diagnosis</Text>
      
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

      <TouchableOpacity onPress={() => navigation.navigate('Home')} style={{marginTop: 20, marginBottom: 50}}>
          <Text style={typography.caption}>Return to Hub</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  card: {
    backgroundColor: colors.surface,
    borderRadius: 20,
    width: '100%',
    marginTop: 30,
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
    borderRadius: 8,
    width: '100%',
    alignItems: 'center',
    shadowColor: colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 8,
  }
});
