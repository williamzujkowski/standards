---
name: graphql-api-design
category: api
difficulty: intermediate
estimated_time: 45 minutes
description: Comprehensive GraphQL API design with Apollo Server, GraphQL Yoga, and Federation v2
version: 1.0.0
---

# GraphQL API Design Skill

## Level 1: Quick Reference (~800 tokens)

### GraphQL vs REST: When to Use GraphQL

**Use GraphQL When:**
- Clients need flexible data fetching (avoid over/under-fetching)
- Multiple client types with different data requirements (mobile, web, IoT)
- Real-time data updates via subscriptions
- Complex data relationships and nested queries
- Rapid frontend iteration without backend changes

**Use REST When:**
- Simple CRUD operations with predictable access patterns
- File uploads/downloads (though GraphQL can handle with multipart)
- HTTP caching is critical (GET requests)
- Team unfamiliarity with GraphQL tooling

### Schema Design Principles

**Core Concepts:**
1. **Type System**: Strongly typed schema defines API contract
2. **Query**: Read operations (like GET)
3. **Mutation**: Write operations (like POST/PUT/DELETE)
4. **Subscription**: Real-time data streams over WebSocket
5. **Resolver**: Function that returns data for a field

**Design Rules:**
- Use nouns for types, verbs for mutations
- Prefer pagination over large lists
- Design for client use cases, not database structure
- Use interfaces for polymorphic types
- Leverage custom scalars (DateTime, Email, URL)

### Essential Checklist

#### Schema Design
- [ ] Define clear type hierarchy (Query, Mutation, Subscription roots)
- [ ] Use descriptive field names and types
- [ ] Add field-level descriptions for documentation
- [ ] Implement input validation with custom scalars
- [ ] Design pagination with cursor-based approach

#### Resolvers & Performance
- [ ] Implement DataLoader for N+1 query prevention
- [ ] Batch database queries within request context
- [ ] Add resolver-level caching strategy
- [ ] Use field-level resolvers only when needed
- [ ] Implement query complexity analysis

#### Authorization & Security
- [ ] Context-based authentication (verify tokens)
- [ ] Field-level authorization with directives
- [ ] Query depth limiting (prevent deeply nested attacks)
- [ ] Query complexity cost analysis
- [ ] Rate limiting per client/operation

#### Federation (Microservices)
- [ ] Define subgraph schemas with `@key` directives
- [ ] Implement reference resolvers for entity resolution
- [ ] Configure Apollo Gateway for schema composition
- [ ] Set up schema registry for version control
- [ ] Monitor federated trace data

#### Error Handling
- [ ] Return structured errors with codes and extensions
- [ ] Distinguish user errors from system errors
- [ ] Implement partial error responses
- [ ] Log errors with correlation IDs
- [ ] Mask sensitive data in error messages

#### Testing
- [ ] Unit test resolvers with mocked data sources
- [ ] Integration test with test database
- [ ] Schema validation with apollo CLI
- [ ] Performance test with realistic queries
- [ ] Security test for common vulnerabilities

### Quick Wins

**Immediate Optimizations:**
1. **DataLoader**: Reduce N+1 queries by 90%+
   ```typescript
   const userLoader = new DataLoader(async (userIds) => {
     const users = await db.users.findMany({ where: { id: { in: userIds } } });
     return userIds.map(id => users.find(u => u.id === id));
   });
   ```

2. **Query Complexity**: Prevent expensive queries
   ```typescript
   const server = new ApolloServer({
     schema,
     plugins: [createComplexityPlugin({ maximumComplexity: 1000 })]
   });
   ```

3. **Response Caching**: Cache at resolver or HTTP level
   ```typescript
   @cacheControl(maxAge: 3600)
   type User { id: ID! name: String! }
   ```

4. **Subscription Filtering**: Reduce unnecessary events
   ```typescript
   subscribe: {
     messageAdded: {
       subscribe: withFilter(
         () => pubsub.asyncIterator('MESSAGE_ADDED'),
         (payload, variables) => payload.channelId === variables.channelId
       )
     }
   }
   ```

---

## Level 2: Implementation Guide (~4500 tokens)

### 1. GraphQL Schema Design Best Practices

#### Type System Fundamentals

**Object Types**: Primary building blocks
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

**Input Types**: For mutations and complex arguments
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

**Enums**: For fixed sets of values
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

**Interfaces**: For polymorphic types
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

**Unions**: For heterogeneous result types
```graphql
union SearchResult = User | Post | Comment

type Query {
  search(query: String!): [SearchResult!]!
}
```

**Custom Scalars**: For domain-specific types
```graphql
scalar DateTime
scalar Email
scalar URL
scalar JSON
scalar PositiveInt
```

#### Query Design Patterns

**Root Query Type**
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

**Cursor-Based Pagination** (Relay spec)
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

#### Mutation Design Patterns

**Input/Payload Pattern**: Consistent structure
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

**Optimistic Response Support**
```graphql
type UpdatePostPayload {
  post: Post
  clientMutationId: String  # Client-provided ID for tracking
  errors: [ValidationError!]
}
```

#### Subscription Design

**Real-Time Events**
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

### 2. Resolvers and DataLoaders

#### Resolver Structure

**Basic Resolvers**
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

**Resolver Best Practices**
1. Keep resolvers thin - delegate to data sources
2. Use TypeScript for type safety
3. Handle errors gracefully
4. Return consistent payload structures
5. Log resolver execution for debugging

#### DataLoader Implementation

**Solving the N+1 Problem**

Without DataLoader (N+1 queries):
```typescript
// For 10 posts, this executes 11 queries!
query {
  posts {           # 1 query
    id
    title
    author {        # 10 queries (one per post)
      name
    }
  }
}
```

With DataLoader (2 queries):
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

**DataLoader in Context**
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

**Using DataLoader in Resolvers**
```typescript
const postResolvers = {
  Post: {
    author: async (parent, _args, context) => {
      return context.loaders.userLoader.load(parent.authorId);
    }
  }
};
```

**Advanced DataLoader Patterns**
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

### 3. Apollo Federation v2

#### Subgraph Design

**Users Subgraph**
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

**Posts Subgraph**
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

**Reference Resolvers**
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

#### Gateway Configuration

**Apollo Gateway Setup**
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

**Managed Federation** (Apollo Studio)
```typescript
const gateway = new ApolloGateway({
  // Use managed federation for production
  async supergraphSdl({ apolloGraphRef }) {
    // Graph ref from Apollo Studio
    return fetchSupergraphSdl(apolloGraphRef);
  }
});
```

### 4. Authentication and Authorization

#### Context-Based Authentication

**JWT Token Verification**
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

**Resolver-Level Authorization**
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

#### Directive-Based Authorization

**Schema Directives**
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

**Directive Implementation**
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

### 5. Subscriptions for Real-Time Data

#### WebSocket Transport

**Apollo Server Subscriptions**
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

**PubSub Implementation**
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

**Subscription Resolvers**
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

### 6. Performance Optimization

#### Caching Strategies

**Apollo Cache Control**
```graphql
type Query {
  user(id: ID!): User @cacheControl(maxAge: 3600)
  posts: [Post!]! @cacheControl(maxAge: 300)
}
```

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

**Redis Response Caching**
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

#### Query Complexity Analysis

**Cost-Based Limiting**
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

#### Pagination Best Practices

**Cursor-Based Pagination**
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

### 7. Error Handling and Validation

#### Structured Error Responses

**Custom Error Classes**
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

**Error Formatting**
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

### 8. Testing GraphQL APIs

#### Unit Testing Resolvers

**Resolver Tests**
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

#### Integration Testing

**GraphQL Server Tests**
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

### 9. Production Deployment

#### Health Checks

**Readiness and Liveness**
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

#### Monitoring and Observability

**Apollo Studio Integration**
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

**Custom Metrics**
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

---

## Level 3: Deep Dive Resources

### Official Documentation
- **Apollo Server**: https://www.apollographql.com/docs/apollo-server/
- **GraphQL.org**: https://graphql.org/learn/
- **GraphQL Yoga**: https://the-guild.dev/graphql/yoga-server
- **Apollo Federation**: https://www.apollographql.com/docs/federation/

### Tools & Libraries
- **DataLoader**: https://github.com/graphql/dataloader
- **GraphQL Code Generator**: https://the-guild.dev/graphql/codegen
- **GraphQL ESLint**: https://the-guild.dev/graphql/eslint
- **Apollo Studio**: https://studio.apollographql.com/

### Books & Courses
- "Production Ready GraphQL" by Marc-André Giroux
- "Learning GraphQL" by Eve Porcello & Alex Banks
- Apollo Odyssey (free courses): https://www.apollographql.com/tutorials/

### Bundled Resources
See `templates/` and `config/` directories for production-ready implementations:
- `graphql-schema.graphql` - Complete schema example
- `resolver-patterns.ts` - Resolver implementation patterns
- `federation-config.yaml` - Apollo Federation setup
- `dataloader-implementation.ts` - DataLoader patterns
- `subscription-server.ts` - Real-time subscriptions
- `apollo-studio.yaml` - Monitoring configuration

