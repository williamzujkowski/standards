---
name: react-native-mobile
category: frontend
difficulty: intermediate
tags: [react-native, mobile, ios, android, cross-platform]
last_updated: 2025-10-17
applies_to: [mobile-apps, hybrid-apps]
---

# React Native Mobile Development

> **Level 1**: Quick Reference (~700-900 tokens)
> **Level 2**: Implementation Guide (~4000-5000 tokens)
> **Level 3**: Deep Dive Resources (external links)

---

## Level 1: Quick Reference

### Core Components

```typescript
import { View, Text, ScrollView, FlatList, Image, TouchableOpacity } from 'react-native';

// Basic Layout
<View style={styles.container}>
  <Text style={styles.title}>Hello World</Text>
  <Image source={require('./logo.png')} style={styles.image} />
  <TouchableOpacity onPress={handlePress}>
    <Text>Press Me</Text>
  </TouchableOpacity>
</View>

// List Rendering (Performance Optimized)
<FlatList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  keyExtractor={item => item.id}
  onEndReached={loadMore}
  onEndReachedThreshold={0.5}
/>

// Scrollable Content
<ScrollView contentContainerStyle={styles.scrollContent}>
  {/* Long content */}
</ScrollView>
```

### Navigation (React Navigation v6)

```typescript
// Stack Navigator
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Navigate Between Screens
navigation.navigate('Details', { itemId: 42 });
navigation.goBack();
```

### Styling

```typescript
import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    fontSize: 16,
    color: '#333',
    fontWeight: 'bold',
  },
});
```

### Platform-Specific Code

```typescript
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  container: {
    marginTop: Platform.OS === 'ios' ? 20 : 0,
    ...Platform.select({
      ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 2 } },
      android: { elevation: 4 },
    }),
  },
});

// Platform-specific files
// Button.ios.tsx
// Button.android.tsx
```

### Essential Checklist

- [ ] Use `FlatList` for long lists (virtualized rendering)
- [ ] Implement `React.memo()` for expensive components
- [ ] Handle safe area insets (notches, status bars)
- [ ] Test on both iOS and Android devices
- [ ] Optimize images (use proper dimensions, formats)
- [ ] Handle keyboard avoiding behavior
- [ ] Implement proper navigation typing
- [ ] Use `useCallback` and `useMemo` appropriately
- [ ] Handle network errors and offline states
- [ ] Add accessibility labels for screen readers

---

## Level 2: Implementation Guide

### 1. Core Components and APIs

#### Layout Components

```typescript
import { View, SafeAreaView, ScrollView, KeyboardAvoidingView } from 'react-native';

// Safe Area (respects notches, status bars)
<SafeAreaView style={styles.safeArea}>
  <View style={styles.content}>
    {/* Content */}
  </View>
</SafeAreaView>

// Keyboard Handling
<KeyboardAvoidingView
  behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
  style={styles.container}
>
  <TextInput placeholder="Type here..." />
</KeyboardAvoidingView>

// Flexbox Layout (default: column)
<View style={{ flex: 1, flexDirection: 'row', justifyContent: 'space-between' }}>
  <View style={{ flex: 1 }}>Left</View>
  <View style={{ flex: 2 }}>Right (wider)</View>
</View>
```

#### Interactive Components

```typescript
import { Button, TouchableOpacity, TouchableHighlight, Pressable } from 'react-native';

// Native Button (limited styling)
<Button title="Press Me" onPress={handlePress} color="#007AFF" />

// Custom Button (full control)
<TouchableOpacity
  onPress={handlePress}
  activeOpacity={0.7}
  disabled={isLoading}
>
  <View style={styles.button}>
    <Text style={styles.buttonText}>Custom Button</Text>
  </View>
</TouchableOpacity>

// Pressable (modern, more control)
<Pressable
  onPress={handlePress}
  onLongPress={handleLongPress}
  style={({ pressed }) => [
    styles.button,
    pressed && styles.buttonPressed
  ]}
>
  {({ pressed }) => (
    <Text style={pressed ? styles.textPressed : styles.text}>
      Press Me
    </Text>
  )}
</Pressable>
```

#### Input Components

```typescript
import { TextInput, Switch } from 'react-native';

// Text Input
<TextInput
  value={text}
  onChangeText={setText}
  placeholder="Enter text..."
  placeholderTextColor="#999"
  autoCapitalize="none"
  autoCorrect={false}
  keyboardType="email-address"
  secureTextEntry={isPassword}
  returnKeyType="done"
  onSubmitEditing={handleSubmit}
  style={styles.input}
/>

// Switch
<Switch
  value={isEnabled}
  onValueChange={setIsEnabled}
  trackColor={{ false: '#767577', true: '#81b0ff' }}
  thumbColor={isEnabled ? '#f5dd4b' : '#f4f3f4'}
/>
```

#### List Components

```typescript
// FlatList (virtualized, best for long lists)
<FlatList
  data={items}
  renderItem={({ item, index }) => <ItemRow item={item} index={index} />}
  keyExtractor={(item, index) => item.id || index.toString()}

  // Performance
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  windowSize={10}
  initialNumToRender={10}

  // Pagination
  onEndReached={loadMore}
  onEndReachedThreshold={0.5}

  // Refresh
  refreshing={isRefreshing}
  onRefresh={handleRefresh}

  // Empty State
  ListEmptyComponent={<EmptyState />}

  // Headers/Footers
  ListHeaderComponent={<Header />}
  ListFooterComponent={<Footer />}

  // Separators
  ItemSeparatorComponent={() => <View style={styles.separator} />}
/>

// SectionList (grouped data)
<SectionList
  sections={[
    { title: 'Category A', data: ['Item 1', 'Item 2'] },
    { title: 'Category B', data: ['Item 3', 'Item 4'] },
  ]}
  renderItem={({ item }) => <Text>{item}</Text>}
  renderSectionHeader={({ section }) => (
    <Text style={styles.header}>{section.title}</Text>
  )}
  keyExtractor={(item, index) => item + index}
/>
```

### 2. Navigation Architecture

#### React Navigation v6 Setup

```typescript
// Installation
// npm install @react-navigation/native @react-navigation/native-stack
// npm install react-native-screens react-native-safe-area-context

import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';

// Type-safe navigation
type RootStackParamList = {
  Home: undefined;
  Profile: { userId: string };
  Settings: { section?: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

// Navigation Props Types
type HomeScreenProps = NativeStackScreenProps<RootStackParamList, 'Home'>;
type ProfileScreenProps = NativeStackScreenProps<RootStackParamList, 'Profile'>;

function HomeScreen({ navigation }: HomeScreenProps) {
  return (
    <View>
      <Button
        title="Go to Profile"
        onPress={() => navigation.navigate('Profile', { userId: '123' })}
      />
    </View>
  );
}

function ProfileScreen({ route, navigation }: ProfileScreenProps) {
  const { userId } = route.params;
  return <Text>User ID: {userId}</Text>;
}

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: { backgroundColor: '#007AFF' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: 'bold' },
        }}
      >
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: 'Welcome' }}
        />
        <Stack.Screen
          name="Profile"
          component={ProfileScreen}
          options={({ route }) => ({ title: `User ${route.params.userId}` })}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

#### Tab Navigation

```typescript
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Ionicons from '@expo/vector-icons/Ionicons';

const Tab = createBottomTabNavigator();

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;

          if (route.name === 'Home') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Settings') {
            iconName = focused ? 'settings' : 'settings-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: 'gray',
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
```

#### Drawer Navigation

```typescript
import { createDrawerNavigator } from '@react-navigation/drawer';

const Drawer = createDrawerNavigator();

function DrawerNavigator() {
  return (
    <Drawer.Navigator
      screenOptions={{
        drawerStyle: { backgroundColor: '#fff', width: 240 },
        drawerActiveTintColor: '#007AFF',
      }}
    >
      <Drawer.Screen name="Home" component={HomeScreen} />
      <Drawer.Screen name="Notifications" component={NotificationsScreen} />
    </Drawer.Navigator>
  );
}
```

### 3. State Management

#### Redux Toolkit

```typescript
// store.ts
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './features/counter/counterSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// counterSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CounterState {
  value: number;
  status: 'idle' | 'loading' | 'failed';
}

const initialState: CounterState = {
  value: 0,
  status: 'idle',
};

export const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
  },
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;
export default counterSlice.reducer;

// Component usage
import { useSelector, useDispatch } from 'react-redux';
import type { RootState, AppDispatch } from './store';
import { increment } from './features/counter/counterSlice';

function Counter() {
  const count = useSelector((state: RootState) => state.counter.value);
  const dispatch = useDispatch<AppDispatch>();

  return (
    <View>
      <Text>{count}</Text>
      <Button title="Increment" onPress={() => dispatch(increment())} />
    </View>
  );
}
```

#### Zustand (Lightweight Alternative)

```typescript
import create from 'zustand';

interface BearState {
  bears: number;
  increasePopulation: () => void;
  removeAllBears: () => void;
}

const useBearStore = create<BearState>((set) => ({
  bears: 0,
  increasePopulation: () => set((state) => ({ bears: state.bears + 1 })),
  removeAllBears: () => set({ bears: 0 }),
}));

function BearCounter() {
  const bears = useBearStore((state) => state.bears);
  return <Text>{bears} bears around here...</Text>;
}

function Controls() {
  const increasePopulation = useBearStore((state) => state.increasePopulation);
  return <Button title="Add Bear" onPress={increasePopulation} />;
}
```

#### React Query (Server State)

```typescript
import { useQuery, useMutation, QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <UserList />
    </QueryClientProvider>
  );
}

function UserList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  const mutation = useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });

  if (isLoading) return <Text>Loading...</Text>;
  if (error) return <Text>Error: {error.message}</Text>;

  return (
    <FlatList
      data={data}
      renderItem={({ item }) => <Text>{item.name}</Text>}
      keyExtractor={(item) => item.id}
    />
  );
}
```

### 4. Styling and Theming

#### StyleSheet API

```typescript
import { StyleSheet, Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  // Responsive sizing
  card: {
    width: width * 0.9,
    padding: 16,
    borderRadius: 8,
    backgroundColor: '#f5f5f5',
  },
  // Absolute positioning
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  // Shadow (iOS)
  shadowCard: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  // Elevation (Android)
  elevatedCard: {
    elevation: 5,
  },
});
```

#### Styled Components

```typescript
import styled from 'styled-components/native';

const Container = styled.View`
  flex: 1;
  background-color: ${props => props.theme.background};
  padding: 16px;
`;

const Title = styled.Text<{ featured?: boolean }>`
  font-size: ${props => props.featured ? '24px' : '18px'};
  font-weight: bold;
  color: ${props => props.theme.text};
  margin-bottom: 8px;
`;

const Button = styled.TouchableOpacity`
  background-color: ${props => props.theme.primary};
  padding: 12px 24px;
  border-radius: 8px;
  align-items: center;
`;

function MyComponent() {
  return (
    <Container>
      <Title featured>Hello</Title>
      <Button onPress={() => {}}>
        <Text>Press</Text>
      </Button>
    </Container>
  );
}
```

#### Responsive Design

```typescript
import { useWindowDimensions } from 'react-native';

function ResponsiveComponent() {
  const { width, height, fontScale } = useWindowDimensions();

  const isSmallDevice = width < 375;
  const isTablet = width >= 768;

  return (
    <View style={{
      padding: isTablet ? 32 : 16,
      fontSize: isSmallDevice ? 14 : 16,
    }}>
      <Text>Responsive Content</Text>
    </View>
  );
}

// Breakpoint helper
const getBreakpoint = (width: number) => {
  if (width < 375) return 'xs';
  if (width < 768) return 'sm';
  if (width < 1024) return 'md';
  return 'lg';
};
```

### 5. Platform-Specific Code

#### Platform API

```typescript
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    marginTop: Platform.OS === 'ios' ? 20 : 0,
    padding: Platform.select({
      ios: 12,
      android: 8,
      default: 10,
    }),
  },
});

// Version checking
if (Platform.Version >= 21) {
  // Android API 21+
}

// Constants
const isIOS = Platform.OS === 'ios';
const isAndroid = Platform.OS === 'android';
```

#### File Extensions

```
// Automatically loaded based on platform
Button.ios.tsx     // iOS implementation
Button.android.tsx // Android implementation
Button.tsx         // Fallback

// Import without extension
import Button from './Button'; // Loads correct version
```

#### Conditional Rendering

```typescript
function PlatformSpecificComponent() {
  return (
    <View>
      {Platform.OS === 'ios' ? (
        <IOSSpecificFeature />
      ) : (
        <AndroidSpecificFeature />
      )}
    </View>
  );
}
```

### 6. Native Modules and Bridges

#### Using Native Modules

```typescript
// Accessing camera
import { Camera } from 'react-native-camera';

<Camera
  style={styles.camera}
  type={Camera.Constants.Type.back}
  flashMode={Camera.Constants.FlashMode.on}
>
  <TouchableOpacity onPress={takePicture}>
    <Text>Take Photo</Text>
  </TouchableOpacity>
</Camera>

// Biometric authentication
import TouchID from 'react-native-touch-id';

async function authenticate() {
  try {
    await TouchID.authenticate('Authenticate to continue');
    // Success
  } catch (error) {
    // Failed or cancelled
  }
}
```

#### Linking to Native APIs

```typescript
import { Linking, Alert } from 'react-native';

// Open URL
Linking.openURL('https://example.com');

// Phone call
Linking.openURL('tel:1234567890');

// Email
Linking.openURL('mailto:support@example.com?subject=Help');

// Deep linking
Linking.addEventListener('url', ({ url }) => {
  // Handle deep link
  const route = url.replace(/.*?:\/\//g, '');
  // Navigate to route
});
```

### 7. Performance Optimization

#### Component Optimization

```typescript
import React, { memo, useCallback, useMemo } from 'react';

// Memoize component (prevent re-renders)
const ExpensiveComponent = memo(({ data }: Props) => {
  return <View>{/* Render data */}</View>;
});

// Memoize callbacks
function ParentComponent() {
  const handlePress = useCallback(() => {
    // Handler logic
  }, []); // Dependencies

  const expensiveValue = useMemo(() => {
    return computeExpensiveValue(data);
  }, [data]);

  return <ExpensiveComponent onPress={handlePress} value={expensiveValue} />;
}
```

#### FlatList Optimization

```typescript
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={keyExtractor}

  // Performance props
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  windowSize={10}
  initialNumToRender={10}
  updateCellsBatchingPeriod={50}

  // Use getItemLayout for fixed-height items
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>

// Memoized render function
const renderItem = useCallback(({ item }) => (
  <MemoizedItemComponent item={item} />
), []);
```

#### InteractionManager

```typescript
import { InteractionManager } from 'react-native';

function Screen() {
  useEffect(() => {
    // Defer heavy tasks until after animations
    InteractionManager.runAfterInteractions(() => {
      // Heavy computation or data loading
      loadData();
    });
  }, []);

  return <View>{/* Screen content */}</View>;
}
```

#### Image Optimization

```typescript
import FastImage from 'react-native-fast-image';

<FastImage
  style={styles.image}
  source={{
    uri: 'https://example.com/image.jpg',
    priority: FastImage.priority.normal,
    cache: FastImage.cacheControl.immutable,
  }}
  resizeMode={FastImage.resizeMode.contain}
/>

// Preload images
FastImage.preload([
  { uri: 'https://example.com/image1.jpg' },
  { uri: 'https://example.com/image2.jpg' },
]);
```

### 8. Testing

#### Jest Unit Tests

```typescript
// Component.test.tsx
import { render, fireEvent } from '@testing-library/react-native';
import Button from './Button';

describe('Button', () => {
  it('renders correctly', () => {
    const { getByText } = render(<Button title="Press Me" />);
    expect(getByText('Press Me')).toBeTruthy();
  });

  it('handles press events', () => {
    const onPress = jest.fn();
    const { getByText } = render(<Button title="Press" onPress={onPress} />);

    fireEvent.press(getByText('Press'));
    expect(onPress).toHaveBeenCalledTimes(1);
  });

  it('shows loading state', () => {
    const { getByTestId } = render(<Button title="Submit" isLoading />);
    expect(getByTestId('loading-indicator')).toBeTruthy();
  });
});
```

#### React Native Testing Library

```typescript
import { render, waitFor, screen } from '@testing-library/react-native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

describe('UserList', () => {
  it('loads and displays users', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <UserList />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeTruthy();
    });
  });
});
```

#### E2E Testing (Detox)

```typescript
// e2e/firstTest.e2e.js
describe('Login Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should show login screen', async () => {
    await expect(element(by.id('login-screen'))).toBeVisible();
  });

  it('should login successfully', async () => {
    await element(by.id('email-input')).typeText('user@example.com');
    await element(by.id('password-input')).typeText('password123');
    await element(by.id('login-button')).tap();

    await expect(element(by.id('home-screen'))).toBeVisible();
  });
});
```

### 9. Accessibility

#### Screen Reader Support

```typescript
<View accessible={true} accessibilityLabel="User profile card">
  <Text>John Doe</Text>
  <Text>Software Engineer</Text>
</View>

<TouchableOpacity
  accessible={true}
  accessibilityLabel="Delete item"
  accessibilityHint="Double tap to delete this item"
  accessibilityRole="button"
  onPress={handleDelete}
>
  <Text>Delete</Text>
</TouchableOpacity>

// Announce dynamic changes
import { AccessibilityInfo } from 'react-native';

AccessibilityInfo.announceForAccessibility('Item added to cart');
```

#### Semantic Labels

```typescript
<View accessibilityRole="header">
  <Text>Section Title</Text>
</View>

<FlatList
  accessibilityRole="list"
  data={items}
  renderItem={({ item }) => (
    <View accessibilityRole="listitem">
      <Text>{item.name}</Text>
    </View>
  )}
/>

<TextInput
  accessibilityLabel="Email address"
  accessibilityHint="Enter your email to sign in"
  autoComplete="email"
/>
```

### 10. Deployment

#### iOS App Store

```bash
# 1. Configure app in App Store Connect
# 2. Update version in ios/YourApp/Info.plist

# 3. Archive and upload
cd ios
pod install
cd ..
npx react-native run-ios --configuration Release

# 4. Xcode: Product > Archive > Upload to App Store
```

#### Android Play Store

```bash
# 1. Generate signing key
keytool -genkeypair -v -storetype PKCS12 -keystore my-release-key.keystore \
  -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000

# 2. Configure gradle (android/app/build.gradle)
# Add signing config

# 3. Build release APK/AAB
cd android
./gradlew bundleRelease

# 4. Upload to Play Console
# Bundle: android/app/build/outputs/bundle/release/app-release.aab
```

#### Over-the-Air (OTA) Updates

```typescript
// Using CodePush
import codePush from 'react-native-code-push';

const App = () => {
  useEffect(() => {
    codePush.sync({
      updateDialog: true,
      installMode: codePush.InstallMode.IMMEDIATE,
    });
  }, []);

  return <YourApp />;
};

export default codePush(App);

// Deploy update
// appcenter codepush release-react -a <ownerName>/<appName> -d Production
```

---

## Level 3: Deep Dive Resources

### Official Documentation

- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [React Navigation](https://reactnavigation.org/docs/getting-started)
- [Expo Documentation](https://docs.expo.dev/)

### Performance

- [React Native Performance Guide](https://reactnative.dev/docs/performance)
- [Profiling React Native](https://reactnative.dev/docs/profiling)

### Testing

- [Testing Library for React Native](https://callstack.github.io/react-native-testing-library/)
- [Detox E2E Framework](https://wix.github.io/Detox/)

### State Management

- [Redux Toolkit](https://redux-toolkit.js.org/)
- [Zustand](https://github.com/pmndrs/zustand)
- [React Query](https://tanstack.com/query/latest)

### Native Modules

- [Native Modules Guide](https://reactnative.dev/docs/native-modules-intro)
- [Turbo Modules](https://reactnative.dev/docs/the-new-architecture/pillars-turbomodules)

### Deployment

- [App Store Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Play Store Policies](https://play.google.com/about/developer-content-policy/)
- [CodePush](https://github.com/microsoft/react-native-code-push)

---

## Quick Links to Templates

- [Screen Component Template](./templates/screen-component.tsx)
- [Navigation Setup](./templates/navigation-setup.tsx)
- [Redux Toolkit Slice](./templates/redux-slice.ts)
- [Component Test](./templates/component.test.tsx)
- [Metro Config](./config/metro.config.js)
- [Deployment Checklist](./resources/deployment-checklist.md)
