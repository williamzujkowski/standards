/**
 * Component Test Template
 * Jest + React Native Testing Library
 */

import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react-native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import UserProfile from './UserProfile';

// Mock navigation
const mockNavigation = {
  navigate: jest.fn(),
  goBack: jest.fn(),
  setOptions: jest.fn(),
};

// Mock API
global.fetch = jest.fn();

// Test suite
describe('UserProfile', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false },
      },
    });
    jest.clearAllMocks();
  });

  const renderComponent = (props = {}) => {
    return render(
      <QueryClientProvider client={queryClient}>
        <UserProfile navigation={mockNavigation as any} {...props} />
      </QueryClientProvider>
    );
  };

  it('renders correctly', () => {
    const { getByText } = renderComponent();
    expect(getByText('User Profile')).toBeTruthy();
  });

  it('displays loading state', () => {
    (global.fetch as jest.Mock).mockImplementation(() => 
      new Promise(() => {}) // Never resolves
    );
    
    const { getByTestId } = renderComponent();
    expect(getByTestId('loading-indicator')).toBeTruthy();
  });

  it('fetches and displays user data', async () => {
    const mockUser = {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
    };

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockUser,
    });

    const { getByText } = renderComponent();

    await waitFor(() => {
      expect(getByText('John Doe')).toBeTruthy();
      expect(getByText('john@example.com')).toBeTruthy();
    });
  });

  it('handles API errors', async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce(
      new Error('Network error')
    );

    const { getByText } = renderComponent();

    await waitFor(() => {
      expect(getByText(/error/i)).toBeTruthy();
    });
  });

  it('handles button press', () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <Button title="Press Me" onPress={onPress} />
    );

    fireEvent.press(getByText('Press Me'));
    expect(onPress).toHaveBeenCalledTimes(1);
  });

  it('handles text input', () => {
    const onChangeText = jest.fn();
    const { getByPlaceholderText } = render(
      <TextInput placeholder="Enter name" onChangeText={onChangeText} />
    );

    const input = getByPlaceholderText('Enter name');
    fireEvent.changeText(input, 'John');
    
    expect(onChangeText).toHaveBeenCalledWith('John');
  });

  it('navigates to detail screen', () => {
    const { getByText } = renderComponent();
    
    fireEvent.press(getByText('View Details'));
    
    expect(mockNavigation.navigate).toHaveBeenCalledWith('Details', {
      userId: expect.any(String),
    });
  });

  it('has proper accessibility labels', () => {
    const { getByLabelText } = renderComponent();
    expect(getByLabelText('User profile card')).toBeTruthy();
  });
});
