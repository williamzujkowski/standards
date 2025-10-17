/**
 * Navigation Setup Template
 * 
 * Complete React Navigation v6 configuration with:
 * - Stack, Tab, and Drawer navigators
 * - TypeScript type safety
 * - Deep linking
 * - Authentication flow
 */

import React, { useEffect, useState } from 'react';
import { ActivityIndicator, View } from 'react-native';
import { NavigationContainer, LinkingOptions } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createDrawerNavigator } from '@react-navigation/drawer';
import Ionicons from '@expo/vector-icons/Ionicons';

// Import screens
import LoginScreen from './screens/LoginScreen';
import HomeScreen from './screens/HomeScreen';
import ProfileScreen from './screens/ProfileScreen';
import SettingsScreen from './screens/SettingsScreen';
import DetailsScreen from './screens/DetailsScreen';

// Navigation Types
export type RootStackParamList = {
  Auth: undefined;
  Main: undefined;
  Details: { itemId: string; title?: string };
  Profile: { userId: string };
};

export type AuthStackParamList = {
  Login: undefined;
  Register: undefined;
  ForgotPassword: undefined;
};

export type MainTabParamList = {
  HomeTab: undefined;
  SearchTab: undefined;
  ProfileTab: undefined;
};

export type HomeStackParamList = {
  Home: undefined;
  Details: { itemId: string };
};

// Create navigators
const RootStack = createNativeStackNavigator<RootStackParamList>();
const AuthStack = createNativeStackNavigator<AuthStackParamList>();
const MainTab = createBottomTabNavigator<MainTabParamList>();
const HomeStack = createNativeStackNavigator<HomeStackParamList>();
const Drawer = createDrawerNavigator();

/**
 * Authentication Stack Navigator
 */
function AuthNavigator() {
  return (
    <AuthStack.Navigator
      screenOptions={{
        headerShown: false,
        animation: 'slide_from_right',
      }}
    >
      <AuthStack.Screen name="Login" component={LoginScreen} />
      <AuthStack.Screen name="Register" component={RegisterScreen} />
      <AuthStack.Screen name="ForgotPassword" component={ForgotPasswordScreen} />
    </AuthStack.Navigator>
  );
}

/**
 * Home Stack Navigator (nested in tabs)
 */
function HomeNavigator() {
  return (
    <HomeStack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: '#007AFF' },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: 'bold' },
      }}
    >
      <HomeStack.Screen 
        name="Home" 
        component={HomeScreen}
        options={{ title: 'Home' }}
      />
      <HomeStack.Screen 
        name="Details" 
        component={DetailsScreen}
        options={({ route }) => ({ 
          title: route.params.title || 'Details' 
        })}
      />
    </HomeStack.Navigator>
  );
}

/**
 * Main Tab Navigator
 */
function MainNavigator() {
  return (
    <MainTab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;

          if (route.name === 'HomeTab') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'SearchTab') {
            iconName = focused ? 'search' : 'search-outline';
          } else if (route.name === 'ProfileTab') {
            iconName = focused ? 'person' : 'person-outline';
          }

          return <Ionicons name={iconName!} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: 'gray',
        tabBarStyle: {
          paddingBottom: 5,
          paddingTop: 5,
          height: 60,
        },
        headerShown: false,
      })}
    >
      <MainTab.Screen 
        name="HomeTab" 
        component={HomeNavigator}
        options={{ title: 'Home' }}
      />
      <MainTab.Screen 
        name="SearchTab" 
        component={SearchScreen}
        options={{ title: 'Search' }}
      />
      <MainTab.Screen 
        name="ProfileTab" 
        component={ProfileScreen}
        options={{ title: 'Profile' }}
      />
    </MainTab.Navigator>
  );
}

/**
 * Drawer Navigator (optional, wraps MainNavigator)
 */
function DrawerNavigator() {
  return (
    <Drawer.Navigator
      screenOptions={{
        drawerStyle: {
          backgroundColor: '#fff',
          width: 280,
        },
        drawerActiveTintColor: '#007AFF',
        drawerInactiveTintColor: '#666',
        headerShown: true,
        headerStyle: { backgroundColor: '#007AFF' },
        headerTintColor: '#fff',
      }}
    >
      <Drawer.Screen 
        name="Main" 
        component={MainNavigator}
        options={{
          title: 'Home',
          drawerIcon: ({ color, size }) => (
            <Ionicons name="home" size={size} color={color} />
          ),
        }}
      />
      <Drawer.Screen 
        name="Settings" 
        component={SettingsScreen}
        options={{
          drawerIcon: ({ color, size }) => (
            <Ionicons name="settings" size={size} color={color} />
          ),
        }}
      />
    </Drawer.Navigator>
  );
}

/**
 * Deep Linking Configuration
 */
const linking: LinkingOptions<RootStackParamList> = {
  prefixes: ['myapp://', 'https://myapp.com'],
  config: {
    screens: {
      Auth: {
        screens: {
          Login: 'login',
          Register: 'register',
        },
      },
      Main: {
        screens: {
          HomeTab: {
            screens: {
              Home: 'home',
              Details: 'details/:itemId',
            },
          },
          SearchTab: 'search',
          ProfileTab: 'profile',
        },
      },
      Profile: 'user/:userId',
    },
  },
};

/**
 * Root Navigator
 * Handles authentication flow
 */
function RootNavigator() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check authentication status on mount
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      // Check AsyncStorage for auth token
      // const token = await AsyncStorage.getItem('authToken');
      // setIsAuthenticated(!!token);
      
      // Simulated for template
      setTimeout(() => {
        setIsAuthenticated(false); // Change based on actual auth
        setIsLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Auth check failed:', error);
      setIsAuthenticated(false);
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <RootStack.Navigator screenOptions={{ headerShown: false }}>
      {isAuthenticated ? (
        <RootStack.Screen name="Main" component={DrawerNavigator} />
      ) : (
        <RootStack.Screen name="Auth" component={AuthNavigator} />
      )}
      
      {/* Modal screens (available in both auth states) */}
      <RootStack.Group screenOptions={{ presentation: 'modal' }}>
        <RootStack.Screen 
          name="Profile" 
          component={ProfileScreen}
          options={{ headerShown: true, title: 'User Profile' }}
        />
      </RootStack.Group>
    </RootStack.Navigator>
  );
}

/**
 * App Component
 * Main entry point with NavigationContainer
 */
export default function App() {
  return (
    <NavigationContainer
      linking={linking}
      fallback={<ActivityIndicator size="large" color="#007AFF" />}
      onReady={() => {
        console.log('Navigation is ready');
      }}
      onStateChange={(state) => {
        // Track navigation changes for analytics
        console.log('Navigation state changed:', state);
      }}
    >
      <RootNavigator />
    </NavigationContainer>
  );
}

/**
 * Navigation Utilities
 */

// Create a navigation ref to use outside of React components
import { createNavigationContainerRef } from '@react-navigation/native';

export const navigationRef = createNavigationContainerRef<RootStackParamList>();

export function navigate(name: keyof RootStackParamList, params?: any) {
  if (navigationRef.isReady()) {
    navigationRef.navigate(name as never, params as never);
  }
}

export function goBack() {
  if (navigationRef.isReady() && navigationRef.canGoBack()) {
    navigationRef.goBack();
  }
}

/**
 * Usage in non-React files:
 * 
 * import { navigate } from './navigation-setup';
 * 
 * // Navigate from anywhere
 * navigate('Details', { itemId: '123' });
 */
