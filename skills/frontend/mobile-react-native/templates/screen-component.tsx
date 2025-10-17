/**
 * Screen Component Template
 *
 * Complete template for a typical React Native screen with:
 * - TypeScript typing
 * - Navigation integration
 * - State management
 * - Loading/error states
 * - Accessibility
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
  SafeAreaView,
} from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';

// Navigation Types
type RootStackParamList = {
  Home: undefined;
  Details: { itemId: string };
  UserScreen: { userId: string; name?: string };
};

type Props = NativeStackScreenProps<RootStackParamList, 'UserScreen'>;

// Data Types
interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
}

interface Post {
  id: string;
  title: string;
  content: string;
  userId: string;
}

/**
 * User Screen Component
 * Displays user profile and their posts
 */
const UserScreen: React.FC<Props> = ({ route, navigation }) => {
  const { userId, name } = route.params;

  // State
  const [user, setUser] = useState<User | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch user data
  const fetchUserData = useCallback(async () => {
    try {
      setError(null);
      const [userResponse, postsResponse] = await Promise.all([
        fetch(`https://api.example.com/users/${userId}`),
        fetch(`https://api.example.com/users/${userId}/posts`),
      ]);

      if (!userResponse.ok || !postsResponse.ok) {
        throw new Error('Failed to fetch data');
      }

      const userData = await userResponse.json();
      const postsData = await postsResponse.json();

      setUser(userData);
      setPosts(postsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, [userId]);

  // Initial load
  useEffect(() => {
    fetchUserData();
  }, [fetchUserData]);

  // Update navigation header
  useEffect(() => {
    if (user) {
      navigation.setOptions({ title: user.name });
    }
  }, [user, navigation]);

  // Pull to refresh
  const handleRefresh = useCallback(() => {
    setIsRefreshing(true);
    fetchUserData();
  }, [fetchUserData]);

  // Navigate to post details
  const handlePostPress = useCallback((postId: string) => {
    navigation.navigate('Details', { itemId: postId });
  }, [navigation]);

  // Render post item
  const renderPost = useCallback(({ item }: { item: Post }) => (
    <TouchableOpacity
      style={styles.postCard}
      onPress={() => handlePostPress(item.id)}
      accessible={true}
      accessibilityRole="button"
      accessibilityLabel={`Post: ${item.title}`}
      accessibilityHint="Double tap to view post details"
    >
      <Text style={styles.postTitle}>{item.title}</Text>
      <Text style={styles.postContent} numberOfLines={2}>
        {item.content}
      </Text>
    </TouchableOpacity>
  ), [handlePostPress]);

  // Key extractor
  const keyExtractor = useCallback((item: Post) => item.id, []);

  // Loading state
  if (isLoading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Loading user data...</Text>
      </View>
    );
  }

  // Error state
  if (error) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>Error: {error}</Text>
        <TouchableOpacity style={styles.retryButton} onPress={fetchUserData}>
          <Text style={styles.retryButtonText}>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  // No user data
  if (!user) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>User not found</Text>
      </View>
    );
  }

  // Main content
  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={posts}
        renderItem={renderPost}
        keyExtractor={keyExtractor}

        // Header (user profile)
        ListHeaderComponent={
          <View
            style={styles.profileSection}
            accessible={true}
            accessibilityRole="header"
          >
            <View style={styles.avatar}>
              <Text style={styles.avatarText}>
                {user.name.charAt(0).toUpperCase()}
              </Text>
            </View>
            <Text style={styles.userName}>{user.name}</Text>
            <Text style={styles.userEmail}>{user.email}</Text>
          </View>
        }

        // Empty state
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>No posts yet</Text>
          </View>
        }

        // Refresh control
        refreshControl={
          <RefreshControl
            refreshing={isRefreshing}
            onRefresh={handleRefresh}
            tintColor="#007AFF"
          />
        }

        // Performance
        removeClippedSubviews={true}
        maxToRenderPerBatch={10}
        windowSize={10}

        // Styling
        contentContainerStyle={styles.listContent}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  listContent: {
    paddingBottom: 20,
  },

  // Profile Section
  profileSection: {
    backgroundColor: '#fff',
    padding: 24,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
    marginBottom: 12,
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  avatarText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  userEmail: {
    fontSize: 16,
    color: '#666',
  },

  // Post Card
  postCard: {
    backgroundColor: '#fff',
    marginHorizontal: 16,
    marginBottom: 12,
    padding: 16,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  postTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  postContent: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },

  // Loading State
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: '#666',
  },

  // Error State
  errorText: {
    fontSize: 16,
    color: '#d32f2f',
    textAlign: 'center',
    marginBottom: 16,
  },
  retryButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  retryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },

  // Empty State
  emptyContainer: {
    padding: 40,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 16,
    color: '#999',
  },
});

export default UserScreen;
