/**
 * Redux Toolkit Slice Template
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../store';

// Types
export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
}

export interface Post {
  id: string;
  title: string;
  content: string;
  userId: string;
  createdAt: string;
}

interface UserState {
  currentUser: User | null;
  users: Record<string, User>;
  posts: Post[];
  isLoading: boolean;
  isLoadingPosts: boolean;
  error: string | null;
  currentPage: number;
  hasMore: boolean;
}

const initialState: UserState = {
  currentUser: null,
  users: {},
  posts: [],
  isLoading: false,
  isLoadingPosts: false,
  error: null,
  currentPage: 1,
  hasMore: true,
};

function getAuthToken(): string {
  return 'your-auth-token';
}

export const fetchCurrentUser = createAsyncThunk(
  'user/fetchCurrentUser',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('https://api.example.com/me', {
        headers: { Authorization: `Bearer ${getAuthToken()}` },
      });
      if (!response.ok) throw new Error('Failed to fetch user');
      return await response.json() as User;
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Error');
    }
  }
);

export const fetchPosts = createAsyncThunk(
  'user/fetchPosts',
  async (page: number, { rejectWithValue }) => {
    try {
      const response = await fetch(`https://api.example.com/posts?page=${page}&limit=20`);
      if (!response.ok) throw new Error('Failed to fetch posts');
      const data = await response.json();
      return { posts: data.posts as Post[], hasMore: data.hasMore as boolean };
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Error');
    }
  }
);

export const createPost = createAsyncThunk(
  'user/createPost',
  async (postData: { title: string; content: string }, { rejectWithValue, getState }) => {
    try {
      const state = getState() as RootState;
      const userId = state.user.currentUser?.id;
      if (!userId) throw new Error('User not authenticated');

      const response = await fetch('https://api.example.com/posts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${getAuthToken()}`,
        },
        body: JSON.stringify({ ...postData, userId }),
      });
      if (!response.ok) throw new Error('Failed to create post');
      return await response.json() as Post;
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Error');
    }
  }
);

export const deletePost = createAsyncThunk(
  'user/deletePost',
  async (postId: string, { rejectWithValue }) => {
    try {
      const response = await fetch(`https://api.example.com/posts/${postId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${getAuthToken()}` },
      });
      if (!response.ok) throw new Error('Failed to delete post');
      return postId;
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Error');
    }
  }
);

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    clearError: (state) => { state.error = null; },
    logout: (state) => {
      state.currentUser = null;
      state.users = {};
      state.posts = [];
      state.error = null;
    },
    updateCurrentUser: (state, action: PayloadAction<Partial<User>>) => {
      if (state.currentUser) {
        state.currentUser = { ...state.currentUser, ...action.payload };
      }
    },
    resetPagination: (state) => {
      state.currentPage = 1;
      state.hasMore = true;
      state.posts = [];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchCurrentUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchCurrentUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentUser = action.payload;
        state.users[action.payload.id] = action.payload;
      })
      .addCase(fetchCurrentUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      .addCase(fetchPosts.pending, (state) => {
        state.isLoadingPosts = true;
        state.error = null;
      })
      .addCase(fetchPosts.fulfilled, (state, action) => {
        state.isLoadingPosts = false;
        state.posts = [...state.posts, ...action.payload.posts];
        state.hasMore = action.payload.hasMore;
        state.currentPage += 1;
      })
      .addCase(fetchPosts.rejected, (state, action) => {
        state.isLoadingPosts = false;
        state.error = action.payload as string;
      })
      .addCase(createPost.pending, (state, action) => {
        const tempPost: Post = {
          id: `temp-${Date.now()}`,
          title: action.meta.arg.title,
          content: action.meta.arg.content,
          userId: state.currentUser?.id || '',
          createdAt: new Date().toISOString(),
        };
        state.posts.unshift(tempPost);
      })
      .addCase(createPost.fulfilled, (state, action) => {
        const tempIndex = state.posts.findIndex(p => p.id.startsWith('temp-'));
        if (tempIndex !== -1) state.posts[tempIndex] = action.payload;
      })
      .addCase(createPost.rejected, (state, action) => {
        state.posts = state.posts.filter(p => !p.id.startsWith('temp-'));
        state.error = action.payload as string;
      })
      .addCase(deletePost.pending, (state, action) => {
        state.posts = state.posts.filter(p => p.id !== action.meta.arg);
      })
      .addCase(deletePost.rejected, (state, action) => {
        state.error = action.payload as string;
      });
  },
});

export const { clearError, logout, updateCurrentUser, resetPagination } = userSlice.actions;
export const selectCurrentUser = (state: RootState) => state.user.currentUser;
export const selectAllPosts = (state: RootState) => state.user.posts;
export default userSlice.reducer;
