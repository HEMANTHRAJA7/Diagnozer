import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, SafeAreaView, ActivityIndicator, StatusBar } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';
import api from '../services/api';

export default function HistoryScreen({ navigation }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/inference/history');
      setHistory(response.data);
    } catch (err) {
      console.error(err);
      setError('Could not retrieve prediction logs.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch history every time the screen is navigated to
  useFocusEffect(
    React.useCallback(() => {
      fetchHistory();
    }, [])
  );

  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString(undefined, { 
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    } catch (e) {
      return dateString;
    }
  };

  const handlePressItem = (item) => {
    // Navigate to Result screen, formatting fields to match resultData requirements
    navigation.navigate('Result', {
      crop: item.crop_type,
      resultData: {
        predictedClass: item.predicted_class,
        confidence: item.confidence,
        heatmapUrl: item.heatmap_url,
        explanation: item.explanation,
        imageType: item.image_type
      }
    });
  };

  const renderItem = ({ item }) => {
    const isMango = item.crop_type.toLowerCase() === 'mango';
    
    return (
      <TouchableOpacity 
        style={styles.card}
        onPress={() => handlePressItem(item)}
        activeOpacity={0.8}
      >
        <View style={styles.cardHeader}>
          <Text style={styles.cropIcon}>{isMango ? '🥭' : '🍈'}</Text>
          <View style={styles.cardTitleBox}>
            <Text style={typography.h3}>{isMango ? 'Mango' : 'Jackfruit'}</Text>
            <Text style={typography.caption}>{formatDate(item.created_at)}</Text>
          </View>
          <View style={styles.confidenceBadge}>
            <Text style={styles.confidenceText}>{(item.confidence * 100).toFixed(0)}%</Text>
          </View>
        </View>

        <View style={styles.cardBody}>
          <Text style={typography.caption}>DIAGNOSIS</Text>
          <Text style={[typography.body, { color: colors.primary, fontWeight: 'bold' }]}>
            {item.predicted_class.replace(/_/g, ' ')}
          </Text>
          {item.image_type && (
            <Text style={[typography.caption, { marginTop: 4 }]}>
              Target: {item.image_type}
            </Text>
          )}
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={colors.background} />
      
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={{ color: colors.primary, fontWeight: '600', fontSize: 16 }}>← Back</Text>
        </TouchableOpacity>
        <Text style={typography.h2}>Scan History</Text>
        <View style={{ width: 50 }} />
      </View>

      {loading ? (
        <View style={styles.centered}>
          <ActivityIndicator size="large" color={colors.primary} />
        </View>
      ) : error ? (
        <View style={styles.centered}>
          <Text style={[typography.body, { color: colors.danger, marginBottom: 20 }]}>{error}</Text>
          <TouchableOpacity style={styles.retryButton} onPress={fetchHistory}>
            <Text style={[typography.button, { color: colors.background }]}>RETRY CONNECTION</Text>
          </TouchableOpacity>
        </View>
      ) : history.length === 0 ? (
        <View style={styles.centered}>
          <Text style={{ fontSize: 50, marginBottom: 15 }}>📋</Text>
          <Text style={typography.h3}>No diagnoses logged yet</Text>
          <Text style={[typography.body, { textAlign: 'center', marginTop: 10, paddingHorizontal: 40 }]}>
            Diagnostic scan operations will populate your ledger automatically.
          </Text>
        </View>
      ) : (
        <FlatList
          data={history}
          keyExtractor={(item) => item._id || item.created_at}
          renderItem={renderItem}
          contentContainerStyle={styles.listContent}
        />
      )}
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
  listContent: {
    padding: 24,
    gap: 16,
  },
  card: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 16,
    padding: 20,
    overflow: 'hidden',
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    paddingBottom: 12,
  },
  cropIcon: {
    fontSize: 28,
    marginRight: 12,
  },
  cardTitleBox: {
    flex: 1,
  },
  confidenceBadge: {
    backgroundColor: colors.surfaceLight,
    borderColor: colors.primary,
    borderWidth: 1.5,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  confidenceText: {
    color: colors.primary,
    fontWeight: 'bold',
    fontSize: 14,
  },
  cardBody: {
    gap: 2,
  },
  centered: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  retryButton: {
    backgroundColor: colors.primary,
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  }
});
