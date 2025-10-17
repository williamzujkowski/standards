/**
 * DataLoader Implementation Patterns
 * Comprehensive examples for solving N+1 queries and optimizing GraphQL performance
 */

import DataLoader from 'dataloader';
import { performance } from 'perf_hooks';

// ============================================================================
// Type Definitions
// ============================================================================

interface User {
  id: string;
  email: string;
  name: string;
  organizationId: string;
}

interface Post {
  id: string;
  title: string;
  content: string;
  authorId: string;
  tags: string[];
}

interface Comment {
  id: string;
  content: string;
  postId: string;
  authorId: string;
}

interface Organization {
  id: string;
  name: string;
}

// ============================================================================
// Basic DataLoader Patterns
// ============================================================================

/**
 * Basic DataLoader: Load entities by ID
 * Batches multiple individual loads into a single database query
 */
export function createUserLoader(db: any): DataLoader<string, User | null> {
  return new DataLoader<string, User | null>(
    async (userIds: readonly string[]) => {
      const count = userIds.length;
      console.log('[DataLoader] Batch loading users:', count);
      const startTime = performance.now();

      // Single query for all user IDs
      const users = await db.users.findMany({
        where: { id: { in: userIds as string[] } }
      });

      const duration = performance.now() - startTime;
      console.log('[DataLoader] Loaded users in ms:', duration);

      // CRITICAL: Return results in the exact same order as input keys
      return userIds.map(id => users.find(user => user.id === id) || null);
    },
    {
      // Configuration options
      cache: true,              // Enable result caching (default: true)
      maxBatchSize: 100,        // Max items per batch
      batchScheduleFn: callback => setTimeout(callback, 10)  // 10ms batch window
    }
  );
}

/**
 * DataLoader with error handling
 */
export function createPostLoader(db: any): DataLoader<string, Post | null> {
  return new DataLoader<string, Post | null>(
    async (postIds: readonly string[]) => {
      try {
        const posts = await db.posts.findMany({
          where: { id: { in: postIds as string[] } }
        });

        return postIds.map(id => {
          const post = posts.find(p => p.id === id);
          if (!post) {
            return null;
          }
          return post;
        });
      } catch (error) {
        console.error('[DataLoader] Error loading posts:', error);
        return postIds.map(() => error);
      }
    }
  );
}

// ============================================================================
// One-to-Many Relationships
// ============================================================================

/**
 * Load posts by author (one-to-many)
 */
export function createPostsByAuthorLoader(db: any): DataLoader<string, Post[]> {
  return new DataLoader<string, Post[]>(
    async (authorIds: readonly string[]) => {
      const count = authorIds.length;
      console.log('[DataLoader] Batch loading posts for authors:', count);

      const posts = await db.posts.findMany({
        where: { authorId: { in: authorIds as string[] } }
      });

      const postsByAuthor = new Map<string, Post[]>();

      authorIds.forEach(authorId => {
        postsByAuthor.set(authorId, []);
      });

      posts.forEach(post => {
        const authorPosts = postsByAuthor.get(post.authorId) || [];
        authorPosts.push(post);
        postsByAuthor.set(post.authorId, authorPosts);
      });

      return authorIds.map(authorId => postsByAuthor.get(authorId) || []);
    }
  );
}

/**
 * Load comments by post (one-to-many with sorting)
 */
export function createCommentsByPostLoader(db: any): DataLoader<string, Comment[]> {
  return new DataLoader<string, Comment[]>(
    async (postIds: readonly string[]) => {
      const comments = await db.comments.findMany({
        where: { postId: { in: postIds as string[] } },
        orderBy: { createdAt: 'asc' }
      });

      const commentsByPost = new Map<string, Comment[]>();

      postIds.forEach(postId => {
        const postComments = comments.filter(c => c.postId === postId);
        commentsByPost.set(postId, postComments);
      });

      return postIds.map(postId => commentsByPost.get(postId) || []);
    }
  );
}

// ============================================================================
// Composite Key DataLoaders
// ============================================================================

interface CompositeKey {
  userId: string;
  postId: string;
}

function serializeKey(key: CompositeKey): string {
  return key.userId + ':' + key.postId;
}

export function createPostLikeLoader(db: any): DataLoader<CompositeKey, boolean> {
  return new DataLoader<CompositeKey, boolean>(
    async (keys: readonly CompositeKey[]) => {
      const likes = await db.likes.findMany({
        where: {
          OR: keys.map(key => ({
            userId: key.userId,
            postId: key.postId
          }))
        }
      });

      const likeSet = new Set(
        likes.map(like => serializeKey({ userId: like.userId, postId: like.postId }))
      );

      return keys.map(key => likeSet.has(serializeKey(key)));
    },
    {
      cacheKeyFn: (key: CompositeKey) => serializeKey(key)
    }
  );
}

// ============================================================================
// Aggregation DataLoaders
// ============================================================================

export function createPostCountLoader(db: any): DataLoader<string, number> {
  return new DataLoader<string, number>(
    async (authorIds: readonly string[]) => {
      const counts = await db.posts.groupBy({
        by: ['authorId'],
        where: { authorId: { in: authorIds as string[] } },
        _count: { id: true }
      });

      const countMap = new Map(
        counts.map(c => [c.authorId, c._count.id])
      );

      return authorIds.map(authorId => countMap.get(authorId) || 0);
    }
  );
}

interface PostStats {
  totalPosts: number;
  publishedPosts: number;
  draftPosts: number;
}

export function createAuthorStatsLoader(db: any): DataLoader<string, PostStats> {
  return new DataLoader<string, PostStats>(
    async (authorIds: readonly string[]) => {
      const posts = await db.posts.findMany({
        where: { authorId: { in: authorIds as string[] } },
        select: { authorId: true, status: true }
      });

      const statsByAuthor = new Map<string, PostStats>();

      authorIds.forEach(authorId => {
        statsByAuthor.set(authorId, {
          totalPosts: 0,
          publishedPosts: 0,
          draftPosts: 0
        });
      });

      posts.forEach(post => {
        const stats = statsByAuthor.get(post.authorId)!;
        stats.totalPosts++;
        if (post.status === 'PUBLISHED') stats.publishedPosts++;
        if (post.status === 'DRAFT') stats.draftPosts++;
      });

      return authorIds.map(authorId => statsByAuthor.get(authorId)!);
    }
  );
}

// ============================================================================
// Cache Management
// ============================================================================

export async function createUser(
  db: any,
  input: any,
  loaders: { userLoader: DataLoader<string, User | null> }
): Promise<User> {
  const user = await db.users.create({ data: input });
  loaders.userLoader.prime(user.id, user);
  return user;
}

export async function updateUser(
  db: any,
  userId: string,
  input: any,
  loaders: { userLoader: DataLoader<string, User | null> }
): Promise<User> {
  const user = await db.users.update({
    where: { id: userId },
    data: input
  });
  loaders.userLoader.clear(userId).prime(userId, user);
  return user;
}

export async function deletePost(
  db: any,
  postId: string,
  loaders: {
    postLoader: DataLoader<string, Post | null>;
    postsByAuthorLoader: DataLoader<string, Post[]>;
  }
): Promise<void> {
  const post = await db.posts.findUnique({ where: { id: postId } });
  await db.posts.delete({ where: { id: postId } });
  loaders.postLoader.clear(postId);
  if (post) {
    loaders.postsByAuthorLoader.clear(post.authorId);
  }
}

// ============================================================================
// DataLoader Factory
// ============================================================================

export interface Loaders {
  userLoader: DataLoader<string, User | null>;
  postLoader: DataLoader<string, Post | null>;
  postsByAuthorLoader: DataLoader<string, Post[]>;
  commentsByPostLoader: DataLoader<string, Comment[]>;
  postLikeLoader: DataLoader<CompositeKey, boolean>;
  postCountLoader: DataLoader<string, number>;
  authorStatsLoader: DataLoader<string, PostStats>;
}

export function createLoaders(db: any): Loaders {
  return {
    userLoader: createUserLoader(db),
    postLoader: createPostLoader(db),
    postsByAuthorLoader: createPostsByAuthorLoader(db),
    commentsByPostLoader: createCommentsByPostLoader(db),
    postLikeLoader: createPostLikeLoader(db),
    postCountLoader: createPostCountLoader(db),
    authorStatsLoader: createAuthorStatsLoader(db)
  };
}

// ============================================================================
// Usage Examples
// ============================================================================

export const exampleResolvers = {
  Query: {
    post: async (_parent: any, { id }: { id: string }, context: any) => {
      return context.loaders.postLoader.load(id);
    }
  },

  Post: {
    author: async (parent: Post, _args: any, context: any) => {
      return context.loaders.userLoader.load(parent.authorId);
    },

    comments: async (parent: Post, _args: any, context: any) => {
      return context.loaders.commentsByPostLoader.load(parent.id);
    },

    isLikedByCurrentUser: async (parent: Post, _args: any, context: any) => {
      if (!context.user) return false;
      return context.loaders.postLikeLoader.load({
        userId: context.user.id,
        postId: parent.id
      });
    }
  },

  User: {
    posts: async (parent: User, _args: any, context: any) => {
      return context.loaders.postsByAuthorLoader.load(parent.id);
    },

    postCount: async (parent: User, _args: any, context: any) => {
      return context.loaders.postCountLoader.load(parent.id);
    },

    stats: async (parent: User, _args: any, context: any) => {
      return context.loaders.authorStatsLoader.load(parent.id);
    }
  }
};
