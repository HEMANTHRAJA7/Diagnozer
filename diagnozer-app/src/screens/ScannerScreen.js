import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image, ActivityIndicator } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';
import api from '../services/api';

export default function ScannerScreen({ route, navigation }) {
  const { crop } = route.params;
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    (async () => {
      const { status } = await ImagePicker.requestCameraPermissionsAsync();
      if (status !== 'granted') {
        alert('Sorry, we need camera permissions to make this work!');
      }
    })();
  }, []);

  const takeProfilePicture = async () => {
    let result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.8,
    });
    if (!result.canceled) setImage(result.assets[0]);
  };

  const pickFromGallery = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      alert('Sorry, we need gallery permissions to pick an image!');
      return;
    }
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.8,
    });
    if (!result.canceled) setImage(result.assets[0]);
  };

  const uploadAndPredict = async () => {
    if (!image) return;
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('crop', crop);
      formData.append('file', {
        uri: image.uri,
        name: 'scan.jpg',
        type: 'image/jpeg',
      });

      const response = await api.post('/inference/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      navigation.replace('Result', { resultData: response.data, crop });
    } catch (error) {
      console.error(error);
      alert('Inference Failed. Check network connection.');
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={[typography.h2, { marginBottom: 20 }]}>Scan {crop.toUpperCase()}</Text>

      {image ? (
        <Image source={{ uri: image.uri }} style={styles.previewContainer} />
      ) : (
        <View style={styles.previewContainer}>
          <Text style={{ fontSize: 50, marginBottom: 10 }}>🔬</Text>
          <Text style={typography.body}>No image selected</Text>
          <Text style={[typography.caption, { marginTop: 5 }]}>Camera or gallery below</Text>
        </View>
      )}

      {loading ? (
        <View style={{ marginTop: 30, alignItems: 'center' }}>
          <ActivityIndicator size="large" color={colors.primary} />
          <Text style={[typography.caption, { marginTop: 15, color: colors.primary }]}>Calculating SHAP array...</Text>
        </View>
      ) : (
        <View style={{ width: '100%', marginTop: 30 }}>
          {/* Source selection buttons */}
          <View style={styles.btnRow}>
            <TouchableOpacity style={[styles.button, { flex: 1, marginRight: 8 }]} onPress={takeProfilePicture}>
              <Text style={styles.btnIcon}>📷</Text>
              <Text style={typography.button}>{image ? 'RETAKE' : 'CAMERA'}</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.buttonOutline, { flex: 1, marginLeft: 8 }]} onPress={pickFromGallery}>
              <Text style={styles.btnIcon}>🖼️</Text>
              <Text style={[typography.button, { color: colors.primary }]}>GALLERY</Text>
            </TouchableOpacity>
          </View>

          {/* Analyse button — only when image is selected */}
          {image && (
            <TouchableOpacity style={styles.analyzeButton} onPress={uploadAndPredict}>
              <Text style={[typography.button, { fontSize: 18 }]}>⚡ ANALYZE NOW</Text>
            </TouchableOpacity>
          )}
        </View>
      )}

      <TouchableOpacity onPress={() => navigation.goBack()} style={{ marginTop: 20 }}>
        <Text style={typography.caption}>← Cancel Scan</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  previewContainer: {
    width: 300,
    height: 300,
    backgroundColor: colors.surface,
    borderRadius: 20,
    borderColor: colors.primary,
    borderWidth: 1,
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
  },
  btnRow: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  button: {
    backgroundColor: colors.primary,
    paddingHorizontal: 20,
    paddingVertical: 18,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonOutline: {
    backgroundColor: 'transparent',
    paddingHorizontal: 20,
    paddingVertical: 18,
    borderRadius: 12,
    borderWidth: 1.5,
    borderColor: colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  analyzeButton: {
    backgroundColor: colors.primary,
    paddingVertical: 20,
    borderRadius: 14,
    alignItems: 'center',
    shadowColor: colors.primary,
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 10,
  },
  btnIcon: {
    fontSize: 22,
    marginBottom: 4,
  },
});
