# Graphql - Reference Implementation

This document contains detailed configuration examples and full code samples extracted from the main skill guide to keep the implementation guide concise.

## Table of Contents

- [1. GraphQL Schema Design Best Practices](#1.-graphql-schema-design-best-practices)
- [Type System Fundamentals](#type-system-fundamentals)
- [Query Design Patterns](#query-design-patterns)
- [Mutation Design Patterns](#mutation-design-patterns)
- [Subscription Design](#subscription-design)
- [2. Resolvers and DataLoaders](#2.-resolvers-and-dataloaders)
- [Resolver Structure](#resolver-structure)
- [DataLoader Implementation](#dataloader-implementation)
- [3. Apollo Federation v2](#3.-apollo-federation-v2)
- [Subgraph Design](#subgraph-design)

---

## Code Examples

### Example 0

```graphql
type User {
  id: ID!
  email: String!
  profile: Profile
  posts: [Post!]!
  createdAt: DateTime!
}

type Profile {
  bio: String
  avatarUrl: URL
  location: String
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  publishedAt: DateTime
  tags: [String!]!
}
```

### Example 1

```graphql
input CreateUserInput {
  email: String!
  password: String!
  profile: ProfileInput
}

input ProfileInput {
  bio: String
  avatarUrl: URL
}

input UpdatePostInput {
  title: String
  content: String
  tags: [String!]
}
```

### Example 2

```graphql
enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

enum UserRole {
  ADMIN
  MODERATOR
  USER
}
```

### Example 3

```graphql
interface Node {
  id: ID!
}

interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}

type User implements Node & Timestamped {
  id: ID!
  email: String!
  createdAt: DateTime!
  updatedAt: DateTime!
}
```

### Example 6

```graphql
type Query {
  # Single entity
  user(id: ID!): User
  post(id: ID!): Post

  # Lists with pagination
  users(first: Int, after: String): UserConnection!
  posts(
    status: PostStatus
    authorId: ID
    first: Int
    after: String
  ): PostConnection!

  # Search
  searchUsers(query: String!): [User!]!

  # Aggregations
  postStats: PostStats!
}
```

### Example 7

```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  cursor: String!
  node: User!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

### Example 8

```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!
}

type CreateUserPayload {
  user: User
  userEdge: UserEdge  # For optimistic updates
  errors: [UserError!]
}

type UserError {
  message: String!
  field: String
  code: String!
}
```

### Example 10

```graphql
type Subscription {
  # Entity-specific
  userUpdated(userId: ID!): User!

  # Filtered streams
  messageAdded(channelId: ID!): Message!

  # Global events
  notificationReceived: Notification!
}

type Message {
  id: ID!
  content: String!
  author: User!
  channel: Channel!
  createdAt: DateTime!
}
```

### Example 11

```typescript
// resolvers/userResolvers.ts
import { GraphQLContext } from '../types';

export const userResolvers = {
  Query: {
    user: async (_parent, { id }, context: GraphQLContext) => {
      return context.dataSources.userAPI.getUserById(id);
    },

    users: async (_parent, { first, after }, context: GraphQLContext) => {
      return context.dataSources.userAPI.getUsers({ first, after });
    }
  },

  Mutation: {
    createUser: async (_parent, { input }, context: GraphQLContext) => {
      // Check authorization
      if (!context.user) {
        throw new Error('Unauthorized');
      }

      // Validate input
      const errors = validateUserInput(input);
      if (errors.length > 0) {
        return { user: null, errors };
      }

      // Create user
      const user = await context.dataSources.userAPI.createUser(input);
      return { user, errors: [] };
    }
  },

  User: {
    // Field resolver for computed/related data
    posts: async (parent, { first, after }, context: GraphQLContext) => {
      return context.loaders.postLoader.loadByAuthor(parent.id, { first, after });
    },

    fullName: (parent) => {
      return `${parent.firstName} ${parent.lastName}`;
    }
  }
};
```

### Example 13

```typescript
// batches-and-caches.ts
import DataLoader from 'dataloader';

// Batch function: receives array of keys, returns array of values
const batchUsers = async (userIds: readonly string[]) => {
  const users = await db.users.findMany({
    where: { id: { in: userIds as string[] } }
  });

  // Must return values in same order as keys
  return userIds.map(id => users.find(user => user.id === id) || null);
};

// Create loader (per-request instance)
export const createUserLoader = () => new DataLoader(batchUsers, {
  cache: true,  // Enable caching (default)
  maxBatchSize: 100  // Limit batch size
});
```

### Example 14

```typescript
// server.ts
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => ({
    user: authenticate(req),
    loaders: {
      userLoader: createUserLoader(),
      postLoader: createPostLoader(),
      commentLoader: createCommentLoader()
    }
  })
});
```

### Example 15

```typescript
const postResolvers = {
  Post: {
    author: async (parent, _args, context) => {
      return context.loaders.userLoader.load(parent.authorId);
    }
  }
};
```

### Example 16

```typescript
// Batch by composite keys
const batchPostsByAuthor = async (authorIds: readonly string[]) => {
  const posts = await db.posts.findMany({
    where: { authorId: { in: authorIds as string[] } }
  });

  return authorIds.map(authorId =>
    posts.filter(post => post.authorId === authorId)
  );
};

// Prime cache from mutation
async createPost(parent, { input }, context) {
  const post = await db.posts.create({ data: input });

  // Prime loader cache to avoid refetch
  context.loaders.postLoader.prime(post.id, post);

  return { post };
}
```

### Example 17

```graphql
# users-subgraph/schema.graphql
extend schema @link(url: "https://specs.apollo.dev/federation/v2.0", import: ["@key", "@shareable"])

type User @key(fields: "id") {
  id: ID!
  email: String!
  name: String!
}

type Query {
  user(id: ID!): User
  users: [User!]!
}
```

### Example 18

```graphql
# posts-subgraph/schema.graphql
extend schema @link(url: "https://specs.apollo.dev/federation/v2.0", import: ["@key", "@external"])

type User @key(fields: "id") {
  id: ID! @external
  posts: [Post!]!
}

type Post @key(fields: "id") {
  id: ID!
  title: String!
  content: String!
  authorId: ID!
  author: User!
}

type Query {
  post(id: ID!): Post
  posts: [Post!]!
}
```

### Example 19

```typescript
// posts-subgraph/resolvers.ts
export const resolvers = {
  User: {
    __resolveReference: async (user: { id: string }) => {
      return { id: user.id };  // Minimal representation
    },

    posts: async (user: { id: string }, _args, context) => {
      return context.dataSources.postAPI.getPostsByAuthor(user.id);
    }
  },

  Post: {
    __resolveReference: async (post: { id: string }, context) => {
      return context.dataSources.postAPI.getPostById(post.id);
    }
  }
};
```

### Example 20

```typescript
// gateway/server.ts
import { ApolloGateway, IntrospectAndCompose } from '@apollo/gateway';
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'users', url: 'http://localhost:4001/graphql' },
      { name: 'posts', url: 'http://localhost:4002/graphql' },
      { name: 'comments', url: 'http://localhost:4003/graphql' }
    ],
    pollIntervalInMs: 10000  // Poll for schema updates
  })
});

const server = new ApolloServer({ gateway });

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 }
});

console.log(`🚀 Gateway ready at ${url}`);
```

### Example 21

```typescript
const gateway = new ApolloGateway({
  // Use managed federation for production
  async supergraphSdl({ apolloGraphRef }) {
    // Graph ref from Apollo Studio
    return fetchSupergraphSdl(apolloGraphRef);
  }
});
```

### Example 22

```typescript
// auth/context.ts
import jwt from 'jsonwebtoken';

interface AuthContext {
  user: { id: string; role: string } | null;
  loaders: DataLoaders;
}

export async function createContext({ req }): Promise<AuthContext> {
  const token = req.headers.authorization?.replace('Bearer ', '');

  let user = null;
  if (token) {
    try {
      user = jwt.verify(token, process.env.JWT_SECRET) as { id: string; role: string };
    } catch (error) {
      console.error('Invalid token:', error);
    }
  }

  return {
    user,
    loaders: createLoaders()
  };
}
```

### Example 23

```typescript
// auth/guards.ts
export function requireAuth(next: GraphQLFieldResolver<any, any, any>) {
  return (parent, args, context: AuthContext, info) => {
    if (!context.user) {
      throw new Error('Unauthorized - authentication required');
    }
    return next(parent, args, context, info);
  };
}

export function requireRole(role: string) {
  return (next: GraphQLFieldResolver<any, any, any>) => {
    return (parent, args, context: AuthContext, info) => {
      if (!context.user) {
        throw new Error('Unauthorized');
      }
      if (context.user.role !== role) {
        throw new Error('Forbidden - insufficient permissions');
      }
      return next(parent, args, context, info);
    };
  };
}

// Usage in resolvers
const resolvers = {
  Mutation: {
    createPost: requireAuth(async (parent, { input }, context) => {
      // User is authenticated
      return createPost(input, context.user.id);
    }),

    deleteUser: requireRole('ADMIN')(async (parent, { id }, context) => {
      // User is admin
      return deleteUser(id);
    })
  }
};
```

### Example 24

```graphql
directive @auth on FIELD_DEFINITION | OBJECT
directive @requireRole(role: String!) on FIELD_DEFINITION

type Query {
  me: User @auth
  users: [User!]! @requireRole(role: "ADMIN")
}

type Mutation {
  deleteUser(id: ID!): User @requireRole(role: "ADMIN")
  updateProfile(input: UpdateProfileInput!): User @auth
}
```

### Example 25

```typescript
// auth/directives.ts
import { mapSchema, getDirective, MapperKind } from '@graphql-tools/utils';
import { GraphQLSchema } from 'graphql';

export function authDirective(schema: GraphQLSchema) {
  return mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
      const authDirective = getDirective(schema, fieldConfig, 'auth')?.[0];

      if (authDirective) {
        const { resolve = defaultFieldResolver } = fieldConfig;

        fieldConfig.resolve = function (source, args, context, info) {
          if (!context.user) {
            throw new Error('Unauthorized');
          }
          return resolve(source, args, context, info);
        };
      }

      return fieldConfig;
    }
  });
}
```

### Example 26

```typescript
// server.ts
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { makeExecutableSchema } from '@graphql-tools/schema';
import express from 'express';

const schema = makeExecutableSchema({ typeDefs, resolvers });

const app = express();
const httpServer = createServer(app);

// WebSocket server for subscriptions
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql'
});

const serverCleanup = useServer({ schema }, wsServer);

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await serverCleanup.dispose();
          }
        };
      }
    }
  ]
});

await server.start();

app.use('/graphql', express.json(), expressMiddleware(server));

httpServer.listen(4000, () => {
  console.log(`🚀 Server ready at http://localhost:4000/graphql`);
});
```

### Example 27

```typescript
// pubsub/index.ts
import { RedisPubSub } from 'graphql-redis-subscriptions';
import Redis from 'ioredis';

const options = {
  host: process.env.REDIS_HOST,
  port: parseInt(process.env.REDIS_PORT || '6379'),
  retryStrategy: (times: number) => Math.min(times * 50, 2000)
};

export const pubsub = new RedisPubSub({
  publisher: new Redis(options),
  subscriber: new Redis(options)
});

// Event types
export const EVENTS = {
  MESSAGE_ADDED: 'MESSAGE_ADDED',
  USER_UPDATED: 'USER_UPDATED',
  NOTIFICATION_RECEIVED: 'NOTIFICATION_RECEIVED'
};
```

### Example 28

```typescript
// resolvers/subscriptions.ts
import { withFilter } from 'graphql-subscriptions';
import { pubsub, EVENTS } from '../pubsub';

export const subscriptionResolvers = {
  Subscription: {
    messageAdded: {
      subscribe: withFilter(
        () => pubsub.asyncIterator(EVENTS.MESSAGE_ADDED),
        (payload, variables, context) => {
          // Filter by channel
          return payload.message.channelId === variables.channelId;
        }
      )
    },

    userUpdated: {
      subscribe: withFilter(
        () => pubsub.asyncIterator(EVENTS.USER_UPDATED),
        (payload, variables, context) => {
          // User receives their own updates
          return context.user?.id === variables.userId;
        }
      )
    }
  },

  Mutation: {
    sendMessage: async (parent, { input }, context) => {
      const message = await createMessage(input);

      // Publish event
      pubsub.publish(EVENTS.MESSAGE_ADDED, { message });

      return { message };
    }
  }
};
```

### Example 30

```typescript
// server.ts
import { ApolloServerPluginCacheControl } from '@apollo/server/plugin/cacheControl';

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginCacheControl({ defaultMaxAge: 60 })
  ]
});
```

### Example 31

```typescript
// cache/redis.ts
import { createClient } from 'redis';

const redis = createClient({ url: process.env.REDIS_URL });

export async function cacheResolver<T>(
  key: string,
  ttl: number,
  fn: () => Promise<T>
): Promise<T> {
  // Check cache
  const cached = await redis.get(key);
  if (cached) {
    return JSON.parse(cached);
  }

  // Execute and cache
  const result = await fn();
  await redis.setEx(key, ttl, JSON.stringify(result));

  return result;
}

// Usage in resolver
async user(parent, { id }, context) {
  return cacheResolver(
    `user:${id}`,
    3600,
    () => context.dataSources.userAPI.getUserById(id)
  );
}
```

### Example 32

```typescript
// plugins/complexity.ts
import { ApolloServerPlugin } from '@apollo/server';
import { getComplexity, simpleEstimator } from 'graphql-query-complexity';

export function complexityPlugin(maxComplexity: number): ApolloServerPlugin {
  return {
    async requestDidStart() {
      return {
        async didResolveOperation({ request, document, schema }) {
          const complexity = getComplexity({
            schema,
            query: document,
            variables: request.variables,
            estimators: [simpleEstimator({ defaultComplexity: 1 })]
          });

          if (complexity > maxComplexity) {
            throw new Error(
              `Query too complex: ${complexity}. Maximum: ${maxComplexity}`
            );
          }
        }
      };
    }
  };
}
```

### Example 33

```typescript
// pagination/cursor.ts
export function encodeCursor(value: string): string {
  return Buffer.from(value).toString('base64');
}

export function decodeCursor(cursor: string): string {
  return Buffer.from(cursor, 'base64').toString('utf-8');
}

export async function paginate<T>(
  query: any,
  { first, after }: { first: number; after?: string }
): Promise<{ edges: Array<{ cursor: string; node: T }>; pageInfo: any }> {
  const limit = first + 1;  // Fetch one extra for hasNextPage

  if (after) {
    query = query.where('id', '>', decodeCursor(after));
  }

  const items = await query.limit(limit).orderBy('id');
  const hasNextPage = items.length > first;

  const edges = items.slice(0, first).map((item: T & { id: string }) => ({
    cursor: encodeCursor(item.id),
    node: item
  }));

  return {
    edges,
    pageInfo: {
      hasNextPage,
      endCursor: edges.length > 0 ? edges[edges.length - 1].cursor : null
    }
  };
}
```

### Example 34

```typescript
// errors/index.ts
import { GraphQLError } from 'graphql';

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
```

### Example 35

```typescript
// server.ts
const server = new ApolloServer({
  schema,
  formatError: (formattedError, error) => {
    // Log internal errors
    if (formattedError.extensions?.code === 'INTERNAL_SERVER_ERROR') {
      console.error('Internal error:', error);

      // Mask details in production
      if (process.env.NODE_ENV === 'production') {
        return {
          message: 'Internal server error',
          extensions: { code: 'INTERNAL_SERVER_ERROR' }
        };
      }
    }

    return formattedError;
  }
});
```

### Example 36

```typescript
// resolvers/user.test.ts
import { userResolvers } from './userResolvers';

describe('User Resolvers', () => {
  const mockContext = {
    dataSources: {
      userAPI: {
        getUserById: jest.fn(),
        createUser: jest.fn()
      }
    },
    loaders: {
      userLoader: {
        load: jest.fn()
      }
    },
    user: { id: '1', role: 'USER' }
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Query.user', () => {
    it('fetches user by id', async () => {
      const mockUser = { id: '1', email: 'test@example.com' };
      mockContext.dataSources.userAPI.getUserById.mockResolvedValue(mockUser);

      const result = await userResolvers.Query.user(
        null,
        { id: '1' },
        mockContext,
        {} as any
      );

      expect(result).toEqual(mockUser);
      expect(mockContext.dataSources.userAPI.getUserById).toHaveBeenCalledWith('1');
    });
  });

  describe('Mutation.createUser', () => {
    it('creates user with valid input', async () => {
      const input = { email: 'new@example.com', password: 'secure123' };
      const mockUser = { id: '2', ...input };
      mockContext.dataSources.userAPI.createUser.mockResolvedValue(mockUser);

      const result = await userResolvers.Mutation.createUser(
        null,
        { input },
        mockContext,
        {} as any
      );

      expect(result.user).toEqual(mockUser);
      expect(result.errors).toHaveLength(0);
    });
  });
});
```

### Example 37

```typescript
// server.test.ts
import { ApolloServer } from '@apollo/server';
import { typeDefs } from './schema';
import { resolvers } from './resolvers';

describe('GraphQL Server', () => {
  let server: ApolloServer;

  beforeAll(async () => {
    server = new ApolloServer({ typeDefs, resolvers });
  });

  afterAll(async () => {
    await server.stop();
  });

  it('executes user query', async () => {
    const result = await server.executeOperation({
      query: `
        query GetUser($id: ID!) {
          user(id: $id) {
            id
            email
          }
        }
      `,
      variables: { id: '1' }
    });

    expect(result.body.kind).toBe('single');
    if (result.body.kind === 'single') {
      expect(result.body.singleResult.errors).toBeUndefined();
      expect(result.body.singleResult.data?.user).toBeDefined();
    }
  });
});
```

### Example 38

```typescript
// health/checks.ts
export async function healthCheck() {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    subgraphs: await checkSubgraphs()
  };

  const isHealthy = Object.values(checks).every(check => check.status === 'ok');

  return {
    status: isHealthy ? 'ok' : 'degraded',
    checks,
    timestamp: new Date().toISOString()
  };
}

app.get('/health', async (req, res) => {
  const health = await healthCheck();
  res.status(health.status === 'ok' ? 200 : 503).json(health);
});
```

### Example 39

```typescript
import { ApolloServerPluginUsageReporting } from '@apollo/server/plugin/usageReporting';

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginUsageReporting({
      sendVariableValues: { all: true },
      sendHeaders: { all: true }
    })
  ]
});
```

### Example 40

```typescript
// metrics/prometheus.ts
import { register, Counter, Histogram } from 'prom-client';

export const resolverDuration = new Histogram({
  name: 'graphql_resolver_duration_seconds',
  help: 'Duration of GraphQL resolver execution',
  labelNames: ['type', 'field']
});

export const resolverErrors = new Counter({
  name: 'graphql_resolver_errors_total',
  help: 'Total number of resolver errors',
  labelNames: ['type', 'field', 'code']
});

app.get('/metrics', (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(register.metrics());
});
```

### Example 41

```python
// TODO: Add basic example for graphql
// This example demonstrates core functionality
```

---

## Additional Resources

See the main SKILL.md file for essential patterns and the official documentation for complete API references.
