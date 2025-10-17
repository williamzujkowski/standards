/**
 * GraphQL Subscription Server Setup
 * WebSocket-based real-time data with Redis PubSub
 */

import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { createServer } from 'http';
import express from 'express';
import cors from 'cors';
import { RedisPubSub } from 'graphql-redis-subscriptions';
import Redis from 'ioredis';
import { withFilter } from 'graphql-subscriptions';

// ============================================================================
// Type Definitions
// ============================================================================

const typeDefs = `#graphql
  type User {
    id: ID!
    username: String!
    online: Boolean!
    lastSeen: String
  }

  type Message {
    id: ID!
    content: String!
    channelId: ID!
    author: User!
    createdAt: String!
  }

  type Channel {
    id: ID!
    name: String!
    members: [User!]!
  }

  type Notification {
    id: ID!
    type: String!
    message: String!
    userId: ID!
    read: Boolean!
    createdAt: String!
  }

  type OnlineStatus {
    userId: ID!
    online: Boolean!
    lastSeen: String
  }

  type TypingIndicator {
    userId: ID!
    channelId: ID!
    username: String!
    typing: Boolean!
  }

  type Query {
    messages(channelId: ID!): [Message!]!
    channels: [Channel!]!
  }

  type Mutation {
    sendMessage(channelId: ID!, content: String!): Message!
    joinChannel(channelId: ID!): Channel!
    leaveChannel(channelId: ID!): Boolean!
    setTyping(channelId: ID!, typing: Boolean!): Boolean!
    markNotificationRead(notificationId: ID!): Notification!
  }

  type Subscription {
    messageAdded(channelId: ID!): Message!
    messageBroadcast: Message!
    userOnlineStatus(userId: ID): OnlineStatus!
    typingIndicator(channelId: ID!): TypingIndicator!
    notificationReceived: Notification!
    channelMemberJoined(channelId: ID!): User!
  }
`;

// ============================================================================
// Redis PubSub Configuration
// ============================================================================

const redisOptions = {
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  retryStrategy: (times: number) => {
    const delay = Math.min(times * 50, 2000);
    return delay;
  }
};

// Create separate Redis clients for publisher and subscriber
const pubsub = new RedisPubSub({
  publisher: new Redis(redisOptions),
  subscriber: new Redis(redisOptions)
});

// Event constants
const EVENTS = {
  MESSAGE_ADDED: 'MESSAGE_ADDED',
  MESSAGE_BROADCAST: 'MESSAGE_BROADCAST',
  USER_ONLINE_STATUS: 'USER_ONLINE_STATUS',
  TYPING_INDICATOR: 'TYPING_INDICATOR',
  NOTIFICATION_RECEIVED: 'NOTIFICATION_RECEIVED',
  CHANNEL_MEMBER_JOINED: 'CHANNEL_MEMBER_JOINED'
};

// ============================================================================
// Resolvers
// ============================================================================

const resolvers = {
  Query: {
    messages: async (_parent: any, { channelId }: { channelId: string }) => {
      // Fetch messages from database
      return [];
    },

    channels: async () => {
      // Fetch channels from database
      return [];
    }
  },

  Mutation: {
    sendMessage: async (
      _parent: any,
      { channelId, content }: { channelId: string; content: string },
      context: any
    ) => {
      if (!context.user) {
        throw new Error('Unauthorized');
      }

      // Create message in database
      const message = {
        id: Math.random().toString(),
        content,
        channelId,
        author: context.user,
        createdAt: new Date().toISOString()
      };

      // Publish to specific channel
      await pubsub.publish(EVENTS.MESSAGE_ADDED, {
        messageAdded: message,
        channelId
      });

      // Publish to all subscribers (broadcast)
      await pubsub.publish(EVENTS.MESSAGE_BROADCAST, {
        messageBroadcast: message
      });

      return message;
    },

    joinChannel: async (
      _parent: any,
      { channelId }: { channelId: string },
      context: any
    ) => {
      if (!context.user) {
        throw new Error('Unauthorized');
      }

      // Add user to channel in database
      const channel = {
        id: channelId,
        name: 'Channel Name',
        members: [context.user]
      };

      // Notify channel members
      await pubsub.publish(EVENTS.CHANNEL_MEMBER_JOINED, {
        channelMemberJoined: context.user,
        channelId
      });

      return channel;
    },

    setTyping: async (
      _parent: any,
      { channelId, typing }: { channelId: string; typing: boolean },
      context: any
    ) => {
      if (!context.user) {
        throw new Error('Unauthorized');
      }

      // Publish typing indicator
      await pubsub.publish(EVENTS.TYPING_INDICATOR, {
        typingIndicator: {
          userId: context.user.id,
          channelId,
          username: context.user.username,
          typing
        },
        channelId
      });

      return true;
    },

    markNotificationRead: async (
      _parent: any,
      { notificationId }: { notificationId: string },
      context: any
    ) => {
      if (!context.user) {
        throw new Error('Unauthorized');
      }

      // Update notification in database
      const notification = {
        id: notificationId,
        type: 'MESSAGE',
        message: 'Notification message',
        userId: context.user.id,
        read: true,
        createdAt: new Date().toISOString()
      };

      return notification;
    }
  },

  Subscription: {
    // Subscribe to messages in a specific channel
    messageAdded: {
      subscribe: withFilter(
        () => pubsub.asyncIterator(EVENTS.MESSAGE_ADDED),
        (payload, variables) => {
          // Filter by channelId
          return payload.channelId === variables.channelId;
        }
      )
    },

    // Subscribe to all messages (broadcast)
    messageBroadcast: {
      subscribe: () => pubsub.asyncIterator(EVENTS.MESSAGE_BROADCAST)
    },

    // Subscribe to user online status
    userOnlineStatus: {
      subscribe: withFilter(
        () => pubsub.asyncIterator(EVENTS.USER_ONLINE_STATUS),
        (payload, variables) => {
          // Filter by specific user if provided
          if (variables.userId) {
            return payload.userOnlineStatus.userId === variables.userId;
          }
          return true;
        }
      )
    },

    // Subscribe to typing indicators in a channel
    typingIndicator: {
      subscribe: withFilter(
        () => pubsub.asyncIterator(EVENTS.TYPING_INDICATOR),
        (payload, variables, context) => {
          // Filter by channelId and exclude own typing events
          return (
            payload.channelId === variables.channelId &&
            payload.typingIndicator.userId !== context.user?.id
          );
        }
      )
    },

    // Subscribe to user notifications
    notificationReceived: {
      subscribe: withFilter(
        () => pubsub.asyncIterator(EVENTS.NOTIFICATION_RECEIVED),
        (payload, _variables, context) => {
          if (!context.user) {
            throw new Error('Unauthorized');
          }
          // Only send notifications to the recipient
          return payload.notificationReceived.userId === context.user.id;
        }
      ),
      resolve: (payload) => payload.notificationReceived
    },

    // Subscribe to channel member joins
    channelMemberJoined: {
      subscribe: withFilter(
        () => pubsub.asyncIterator(EVENTS.CHANNEL_MEMBER_JOINED),
        (payload, variables) => {
          return payload.channelId === variables.channelId;
        }
      )
    }
  }
};

// ============================================================================
// Schema Creation
// ============================================================================

const schema = makeExecutableSchema({ typeDefs, resolvers });

// ============================================================================
// Server Setup
// ============================================================================

export async function createSubscriptionServer() {
  const app = express();
  const httpServer = createServer(app);

  // WebSocket server for subscriptions
  const wsServer = new WebSocketServer({
    server: httpServer,
    path: '/graphql'
  });

  // Context function for WebSocket connections
  const getSubscriptionContext = (ctx: any) => {
    // Extract token from connection params
    const token = ctx.connectionParams?.authorization?.replace('Bearer ', '');

    // Verify token and return user
    let user = null;
    if (token) {
      try {
        user = verifyToken(token);
      } catch (error) {
        console.error('Invalid token:', error);
      }
    }

    return { user };
  };

  // Setup WebSocket server with graphql-ws
  const serverCleanup = useServer(
    {
      schema,
      context: getSubscriptionContext,

      // Connection lifecycle
      onConnect: async (ctx) => {
        console.log('Client connected:', ctx.connectionParams);
      },

      onDisconnect: async (ctx) => {
        console.log('Client disconnected');

        // Publish user offline status
        const user = getSubscriptionContext(ctx).user;
        if (user) {
          await pubsub.publish(EVENTS.USER_ONLINE_STATUS, {
            userOnlineStatus: {
              userId: user.id,
              online: false,
              lastSeen: new Date().toISOString()
            }
          });
        }
      },

      onSubscribe: async (_ctx, message) => {
        console.log('Subscription started:', message.payload.operationName);
      },

      onComplete: async (_ctx, message) => {
        console.log('Subscription completed');
      }
    },
    wsServer
  );

  // Apollo Server for HTTP operations
  const apolloServer = new ApolloServer({
    schema,
    plugins: [
      // Proper shutdown for HTTP server
      ApolloServerPluginDrainHttpServer({ httpServer }),

      // Proper shutdown for WebSocket server
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

  await apolloServer.start();

  // Express middleware
  app.use(
    '/graphql',
    cors({
      origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
      credentials: true
    }),
    express.json(),
    expressMiddleware(apolloServer, {
      context: async ({ req }) => {
        const token = req.headers.authorization?.replace('Bearer ', '');
        let user = null;

        if (token) {
          try {
            user = verifyToken(token);
          } catch (error) {
            console.error('Invalid token:', error);
          }
        }

        return { user };
      }
    })
  );

  // Health check endpoint
  app.get('/health', (_req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
  });

  const PORT = process.env.PORT || 4000;

  httpServer.listen(PORT, () => {
    console.log('Server ready at http://localhost:' + PORT + '/graphql');
    console.log('Subscriptions ready at ws://localhost:' + PORT + '/graphql');
  });

  return { httpServer, apolloServer, serverCleanup };
}

// ============================================================================
// Helper Functions
// ============================================================================

function verifyToken(token: string): { id: string; username: string } | null {
  // Implement JWT verification
  return { id: '1', username: 'testuser' };
}

// ============================================================================
// Client Usage Examples
// ============================================================================

const clientExamples = `
// Apollo Client Setup
import { ApolloClient, InMemoryCache, HttpLink, split } from '@apollo/client';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { getMainDefinition } from '@apollo/client/utilities';
import { createClient } from 'graphql-ws';

const httpLink = new HttpLink({
  uri: 'http://localhost:4000/graphql',
  headers: {
    authorization: 'Bearer YOUR_TOKEN'
  }
});

const wsLink = new GraphQLWsLink(
  createClient({
    url: 'ws://localhost:4000/graphql',
    connectionParams: {
      authorization: 'Bearer YOUR_TOKEN'
    }
  })
);

// Split between HTTP and WebSocket
const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  httpLink
);

const client = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache()
});

// Subscription Usage
import { gql, useSubscription } from '@apollo/client';

const MESSAGE_SUBSCRIPTION = gql\`
  subscription OnMessageAdded($channelId: ID!) {
    messageAdded(channelId: $channelId) {
      id
      content
      author {
        username
      }
      createdAt
    }
  }
\`;

function ChatMessages({ channelId }) {
  const { data, loading } = useSubscription(MESSAGE_SUBSCRIPTION, {
    variables: { channelId }
  });

  if (loading) return <div>Loading...</div>;

  return <div>{data?.messageAdded?.content}</div>;
}
`;

// ============================================================================
// Production Considerations
// ============================================================================

const productionNotes = `
Production Checklist:

1. Connection Management:
   - Implement connection limits
   - Add rate limiting per connection
   - Handle connection drops gracefully
   - Implement reconnection logic on client

2. Scalability:
   - Use Redis Cluster for PubSub
   - Implement sticky sessions for WebSocket
   - Use load balancer with WebSocket support
   - Consider using managed service (AWS AppSync, Hasura)

3. Security:
   - Validate all subscription filters
   - Implement per-subscription authorization
   - Add rate limiting for subscriptions
   - Sanitize subscription payloads

4. Monitoring:
   - Track active connections
   - Monitor subscription performance
   - Log subscription errors
   - Track PubSub message volume

5. Testing:
   - Test connection lifecycle
   - Test filter conditions
   - Test under load
   - Test reconnection scenarios
`;

// Start server if run directly
if (require.main === module) {
  createSubscriptionServer().catch(console.error);
}

export { createSubscriptionServer, pubsub, EVENTS };
