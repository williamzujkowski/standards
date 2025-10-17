/**
 * GraphQL Resolver Implementation Patterns
 * Demonstrates best practices for resolver structure, DataLoader usage,
 * authorization, and error handling
 */

import { GraphQLError } from 'graphql';
import DataLoader from 'dataloader';

// ============================================================================
// Type Definitions
// ============================================================================

interface User {
  id: string;
  email: string;
  username: string;
  role: UserRole;
  createdAt: Date;
  updatedAt: Date;
}

enum UserRole {
  ADMIN = 'ADMIN',
  MODERATOR = 'MODERATOR',
  USER = 'USER',
  GUEST = 'GUEST'
}

interface Post {
  id: string;
  title: string;
  content: string;
  authorId: string;
  status: PostStatus;
  createdAt: Date;
  updatedAt: Date;
}

enum PostStatus {
  DRAFT = 'DRAFT',
  PUBLISHED = 'PUBLISHED',
  ARCHIVED = 'ARCHIVED'
}

interface GraphQLContext {
  user: User | null;
  loaders: {
    userLoader: DataLoader<string, User | null>;
    postLoader: DataLoader<string, Post | null>;
    postsByAuthorLoader: DataLoader<string, Post[]>;
  };
  dataSources: {
    userAPI: UserAPI;
    postAPI: PostAPI;
  };
}

// ============================================================================
// Error Handling
// ============================================================================

export class AuthenticationError extends GraphQLError {
  constructor(message = 'Authentication required') {
    super(message, {
      extensions: {
        code: 'UNAUTHENTICATED',
        http: { status: 401 }
      }
    });
  }
}

export class ForbiddenError extends GraphQLError {
  constructor(message = 'Insufficient permissions') {
    super(message, {
      extensions: {
        code: 'FORBIDDEN',
        http: { status: 403 }
      }
    });
  }
}

export class ValidationError extends GraphQLError {
  constructor(message: string, field?: string) {
    super(message, {
      extensions: {
        code: 'VALIDATION_ERROR',
        field,
        http: { status: 400 }
      }
    });
  }
}

export class NotFoundError extends GraphQLError {
  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`, {
      extensions: {
        code: 'NOT_FOUND',
        resource,
        id,
        http: { status: 404 }
      }
    });
  }
}

// ============================================================================
// Authorization Guards
// ============================================================================

export function requireAuth(context: GraphQLContext): void {
  if (!context.user) {
    throw new AuthenticationError();
  }
}

export function requireRole(context: GraphQLContext, role: UserRole): void {
  requireAuth(context);
  if (context.user!.role !== role) {
    throw new ForbiddenError(`Requires role: ${role}`);
  }
}

export function requireOwnership(
  context: GraphQLContext,
  resourceOwnerId: string
): void {
  requireAuth(context);
  if (context.user!.id !== resourceOwnerId && context.user!.role !== UserRole.ADMIN) {
    throw new ForbiddenError('You can only modify your own resources');
  }
}

// ============================================================================
// DataLoader Implementations
// ============================================================================

// Batch function for loading users by ID
export async function batchUsers(userIds: readonly string[]): Promise<(User | null)[]> {
  // Simulated database call
  const users = await db.users.findMany({
    where: { id: { in: userIds as string[] } }
  });

  // CRITICAL: Return values in same order as input keys
  return userIds.map(id => users.find(user => user.id === id) || null);
}

// Batch function for loading posts by ID
export async function batchPosts(postIds: readonly string[]): Promise<(Post | null)[]> {
  const posts = await db.posts.findMany({
    where: { id: { in: postIds as string[] } }
  });

  return postIds.map(id => posts.find(post => post.id === id) || null);
}

// Batch function for loading posts by author (one-to-many)
export async function batchPostsByAuthor(
  authorIds: readonly string[]
): Promise<Post[][]> {
  const posts = await db.posts.findMany({
    where: { authorId: { in: authorIds as string[] } }
  });

  // Group posts by authorId
  return authorIds.map(authorId =>
    posts.filter(post => post.authorId === authorId)
  );
}

// Create DataLoaders (per-request instances)
export function createLoaders() {
  return {
    userLoader: new DataLoader(batchUsers, {
      cache: true,
      maxBatchSize: 100
    }),

    postLoader: new DataLoader(batchPosts, {
      cache: true,
      maxBatchSize: 100
    }),

    postsByAuthorLoader: new DataLoader(batchPostsByAuthor, {
      cache: true,
      maxBatchSize: 50
    })
  };
}

// ============================================================================
// Query Resolvers
// ============================================================================

export const queryResolvers = {
  // Get current authenticated user
  me: async (_parent: any, _args: any, context: GraphQLContext) => {
    requireAuth(context);
    return context.user;
  },

  // Get user by ID
  user: async (
    _parent: any,
    { id }: { id: string },
    context: GraphQLContext
  ): Promise<User | null> => {
    // Use DataLoader for batching and caching
    return context.loaders.userLoader.load(id);
  },

  // Get paginated list of users
  users: async (
    _parent: any,
    { first = 10, after, role }: { first?: number; after?: string; role?: UserRole },
    context: GraphQLContext
  ) => {
    requireRole(context, UserRole.ADMIN);

    return context.dataSources.userAPI.getUsers({ first, after, role });
  },

  // Get post by ID or slug
  post: async (
    _parent: any,
    { id, slug }: { id?: string; slug?: string },
    context: GraphQLContext
  ): Promise<Post | null> => {
    if (id) {
      return context.loaders.postLoader.load(id);
    }

    if (slug) {
      return context.dataSources.postAPI.getPostBySlug(slug);
    }

    throw new ValidationError('Must provide either id or slug');
  },

  // Get paginated posts with filters
  posts: async (
    _parent: any,
    {
      first = 10,
      after,
      filters
    }: {
      first?: number;
      after?: string;
      filters?: { status?: PostStatus; authorId?: string };
    },
    context: GraphQLContext
  ) => {
    return context.dataSources.postAPI.getPosts({ first, after, filters });
  }
};

// ============================================================================
// Mutation Resolvers
// ============================================================================

export const mutationResolvers = {
  // Create new post
  createPost: async (
    _parent: any,
    { input }: { input: { title: string; content: string; status?: PostStatus } },
    context: GraphQLContext
  ) => {
    requireAuth(context);

    // Validate input
    if (!input.title || input.title.length < 3) {
      return {
        post: null,
        errors: [{
          message: 'Title must be at least 3 characters',
          field: 'title',
          code: 'VALIDATION_ERROR'
        }]
      };
    }

    // Create post
    const post = await context.dataSources.postAPI.createPost({
      ...input,
      authorId: context.user!.id
    });

    // Prime DataLoader cache to avoid refetch
    context.loaders.postLoader.prime(post.id, post);

    return {
      post,
      errors: []
    };
  },

  // Update existing post
  updatePost: async (
    _parent: any,
    {
      id,
      input
    }: {
      id: string;
      input: { title?: string; content?: string; status?: PostStatus };
    },
    context: GraphQLContext
  ) => {
    requireAuth(context);

    // Load post to check ownership
    const post = await context.loaders.postLoader.load(id);
    if (!post) {
      throw new NotFoundError('Post', id);
    }

    requireOwnership(context, post.authorId);

    // Update post
    const updatedPost = await context.dataSources.postAPI.updatePost(id, input);

    // Update DataLoader cache
    context.loaders.postLoader.clear(id).prime(id, updatedPost);

    return {
      post: updatedPost,
      errors: []
    };
  },

  // Delete post
  deletePost: async (
    _parent: any,
    { id }: { id: string },
    context: GraphQLContext
  ) => {
    requireAuth(context);

    const post = await context.loaders.postLoader.load(id);
    if (!post) {
      throw new NotFoundError('Post', id);
    }

    requireOwnership(context, post.authorId);

    await context.dataSources.postAPI.deletePost(id);

    // Clear from cache
    context.loaders.postLoader.clear(id);

    return {
      success: true,
      deletedId: id,
      errors: []
    };
  },

  // Like a post
  likePost: async (
    _parent: any,
    { postId }: { postId: string },
    context: GraphQLContext
  ) => {
    requireAuth(context);

    const post = await context.dataSources.postAPI.likePost(
      postId,
      context.user!.id
    );

    // Update cache
    context.loaders.postLoader.clear(postId).prime(postId, post);

    return {
      post,
      errors: []
    };
  }
};

// ============================================================================
// Field Resolvers
// ============================================================================

export const userFieldResolvers = {
  // Resolve user's posts
  posts: async (
    parent: User,
    { first = 10, after, status }: { first?: number; after?: string; status?: PostStatus },
    context: GraphQLContext
  ) => {
    // Use DataLoader for efficient batching
    const allPosts = await context.loaders.postsByAuthorLoader.load(parent.id);

    // Filter by status if provided
    const filteredPosts = status
      ? allPosts.filter(post => post.status === status)
      : allPosts;

    // Apply pagination
    return paginatePosts(filteredPosts, { first, after });
  },

  // Computed field: full name
  fullName: (parent: User & { firstName?: string; lastName?: string }) => {
    return `${parent.firstName || ''} ${parent.lastName || ''}`.trim();
  }
};

export const postFieldResolvers = {
  // Resolve post author
  author: async (parent: Post, _args: any, context: GraphQLContext) => {
    // Use DataLoader to batch author fetches
    return context.loaders.userLoader.load(parent.authorId);
  },

  // Computed field: reading time
  readingTimeMinutes: (parent: Post) => {
    const wordsPerMinute = 200;
    const wordCount = parent.content.split(/\s+/).length;
    return Math.ceil(wordCount / wordsPerMinute);
  },

  // Computed field: excerpt
  excerpt: (parent: Post) => {
    if (parent.content.length <= 200) {
      return parent.content;
    }
    return parent.content.substring(0, 200) + '...';
  }
};

// ============================================================================
// Subscription Resolvers
// ============================================================================

import { withFilter } from 'graphql-subscriptions';
import { pubsub } from '../pubsub';

const EVENTS = {
  POST_PUBLISHED: 'POST_PUBLISHED',
  COMMENT_ADDED: 'COMMENT_ADDED',
  NOTIFICATION_RECEIVED: 'NOTIFICATION_RECEIVED'
};

export const subscriptionResolvers = {
  // Subscribe to published posts (optionally filtered by author)
  postPublished: {
    subscribe: withFilter(
      () => pubsub.asyncIterator(EVENTS.POST_PUBLISHED),
      (payload, variables, context) => {
        // Filter by authorId if provided
        if (variables.authorId) {
          return payload.post.authorId === variables.authorId;
        }
        return true;
      }
    )
  },

  // Subscribe to comments on a specific post
  commentAdded: {
    subscribe: withFilter(
      () => pubsub.asyncIterator(EVENTS.COMMENT_ADDED),
      (payload, variables) => {
        return payload.comment.postId === variables.postId;
      }
    )
  },

  // Subscribe to user notifications
  notificationReceived: {
    subscribe: withFilter(
      () => pubsub.asyncIterator(EVENTS.NOTIFICATION_RECEIVED),
      (payload, _variables, context) => {
        requireAuth(context);
        return payload.notification.userId === context.user!.id;
      }
    )
  }
};

// ============================================================================
// Complete Resolver Map
// ============================================================================

export const resolvers = {
  Query: queryResolvers,
  Mutation: mutationResolvers,
  Subscription: subscriptionResolvers,
  User: userFieldResolvers,
  Post: postFieldResolvers
};

// ============================================================================
// Helper Functions
// ============================================================================

function paginatePosts(
  posts: Post[],
  { first, after }: { first: number; after?: string }
) {
  let startIndex = 0;

  if (after) {
    const afterIndex = posts.findIndex(post => post.id === after);
    if (afterIndex !== -1) {
      startIndex = afterIndex + 1;
    }
  }

  const endIndex = startIndex + first;
  const edges = posts.slice(startIndex, endIndex).map(post => ({
    cursor: post.id,
    node: post
  }));

  return {
    edges,
    pageInfo: {
      hasNextPage: endIndex < posts.length,
      hasPreviousPage: startIndex > 0,
      startCursor: edges[0]?.cursor,
      endCursor: edges[edges.length - 1]?.cursor
    },
    totalCount: posts.length
  };
}

// Simulated database (replace with actual DB)
const db = {
  users: {
    findMany: async ({ where }: any) => [] as User[],
    findOne: async ({ where }: any) => null as User | null
  },
  posts: {
    findMany: async ({ where }: any) => [] as Post[],
    findOne: async ({ where }: any) => null as Post | null
  }
};

// Simulated data sources
class UserAPI {
  async getUserById(id: string): Promise<User | null> {
    return null;
  }

  async getUsers({ first, after, role }: any) {
    return { edges: [], pageInfo: {}, totalCount: 0 };
  }
}

class PostAPI {
  async getPostBySlug(slug: string): Promise<Post | null> {
    return null;
  }

  async getPosts({ first, after, filters }: any) {
    return { edges: [], pageInfo: {}, totalCount: 0 };
  }

  async createPost(input: any): Promise<Post> {
    return {} as Post;
  }

  async updatePost(id: string, input: any): Promise<Post> {
    return {} as Post;
  }

  async deletePost(id: string): Promise<void> {}

  async likePost(postId: string, userId: string): Promise<Post> {
    return {} as Post;
  }
}
