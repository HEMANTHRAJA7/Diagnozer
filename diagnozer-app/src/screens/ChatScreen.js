import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, KeyboardAvoidingView, Platform, ActivityIndicator } from 'react-native';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';
import api from '../services/api';

export default function ChatScreen({ navigation }) {
    const [msg, setMsg] = useState('');
    const [chatLog, setChatLog] = useState([
        { role: 'bot', text: 'Diagnostic system initialized. Using your recent history, how can I assist you with treatments?' }
    ]);
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!msg.trim()) return;
        
        const userText = msg.trim();
        setChatLog(prev => [...prev, { role: 'user', text: userText }]);
        setMsg('');
        setLoading(true);

        try {
            const response = await api.post('/chat/', { message: userText });
            setChatLog(prev => [...prev, { role: 'bot', text: response.data.reply }]);
        } catch (error) {
            setChatLog(prev => [...prev, { role: 'bot', text: 'Error connecting to Gemini mainframe.' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity onPress={() => navigation.goBack()}>
                    <Text style={{color: colors.primary}}>← Back</Text>
                </TouchableOpacity>
                <Text style={typography.h3}>AI Assistant</Text>
                <View style={{width: 50}} />
            </View>

            <ScrollView style={styles.chatArea} contentContainerStyle={{padding: 20}}>
                {chatLog.map((chat, idx) => (
                    <View key={idx} style={[styles.bubble, chat.role === 'user' ? styles.userBubble : styles.botBubble]}>
                        <Text style={validationText(chat.role)}>{chat.text}</Text>
                    </View>
                ))}
                {loading && <ActivityIndicator color={colors.primary} style={{alignSelf: 'flex-start', marginLeft: 10}} />}
            </ScrollView>

            <View style={styles.inputRow}>
                <TextInput 
                    style={styles.input}
                    placeholder="Ask about treatments..."
                    placeholderTextColor={colors.textSecondary}
                    value={msg}
                    onChangeText={setMsg}
                    multiline
                />
                <TouchableOpacity style={styles.sendButton} onPress={sendMessage}>
                    <Text style={{color: colors.background, fontWeight: 'bold'}}>SEND</Text>
                </TouchableOpacity>
            </View>
        </KeyboardAvoidingView>
    );
}

const validationText = (role) => {
    return role === 'user' ? {...typography.body, color: colors.background} : typography.body;
};

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: colors.background },
    header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: 20, paddingTop: 50, borderBottomWidth: 1, borderColor: colors.border },
    chatArea: { flex: 1 },
    bubble: { maxWidth: '80%', padding: 15, borderRadius: 15, marginBottom: 15 },
    userBubble: { alignSelf: 'flex-end', backgroundColor: colors.primary, borderBottomRightRadius: 0 },
    botBubble: { alignSelf: 'flex-start', backgroundColor: colors.surfaceLight, borderBottomLeftRadius: 0, borderWidth: 1, borderColor: colors.border },
    inputRow: { flexDirection: 'row', padding: 15, borderTopWidth: 1, borderColor: colors.surface, marginBottom: 20 },
    input: { flex: 1, backgroundColor: colors.surface, color: colors.text, padding: 15, borderRadius: 20, borderWidth: 1, borderColor: colors.border },
    sendButton: { backgroundColor: colors.primary, paddingHorizontal: 20, justifyContent: 'center', borderRadius: 20, marginLeft: 10 }
});
