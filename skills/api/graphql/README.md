# GraphQL API Design Skill

Production-ready GraphQL skill covering Apollo Server, GraphQL Yoga, and Federation v2.

## Structure

```
skills/api/graphql/
├── SKILL.md                           # Main skill content (1,241 lines)
├── templates/
│   ├── graphql-schema.graphql         # Complete schema example (434 lines)
│   ├── resolver-patterns.ts           # Resolver implementations (580 lines)
│   ├── federation-config.yaml         # Apollo Federation setup (431 lines)
│   ├── dataloader-implementation.ts   # DataLoader patterns (365 lines)
│   └── subscription-server.ts         # Real-time subscriptions (575 lines)
├── config/
│   └── apollo-studio.yaml             # Apollo Studio integration (548 lines)
└── README.md                          # This file

Total: 4,174 lines of production-ready GraphQL content
```

## Skill Content

### Level 1: Quick Reference (~800 tokens)
- GraphQL vs REST comparison
- Schema design principles
- Essential checklist (types, resolvers, DataLoaders, authorization)
- Quick wins for immediate optimization

### Level 2: Implementation Guide (~4,500 tokens)
1. **GraphQL Schema Design** - Types, queries, mutations, subscriptions
2. **Resolvers and DataLoaders** - Solving N+1 problems
3. **Apollo Federation v2** - Subgraphs, gateway, managed federation
4. **Authentication & Authorization** - Context-based, directive-based
5. **Subscriptions** - Real-time data with WebSocket
6. **Performance Optimization** - Caching, complexity, pagination
7. **Error Handling** - Structured errors, validation
8. **Testing** - Unit tests, integration tests
9. **Production Deployment** - Health checks, monitoring

### Level 3: Deep Dive Resources
- Official documentation links
- Tools and libraries
- Books and courses
- Bundled templates and configurations

## Bundled Resources

### 1. graphql-schema.graphql
Complete GraphQL schema demonstrating:
- Custom scalars (DateTime, Email, URL)
- Type system (objects, interfaces, unions, enums)
- Relay-spec pagination
- Federation directives
- Authorization directives

### 2. resolver-patterns.ts
TypeScript resolver implementations showing:
- Query, mutation, and subscription resolvers
- Field-level resolvers
- Authorization guards
- Error handling
- DataLoader integration

### 3. federation-config.yaml
Apollo Federation v2 setup including:
- Gateway configuration
- Subgraph definitions
- Apollo Studio integration
- Caching strategies
- Security settings

### 4. dataloader-implementation.ts
Comprehensive DataLoader patterns:
- Basic entity loading
- One-to-many relationships
- Composite keys
- Aggregations
- Cache management

### 5. subscription-server.ts
Real-time GraphQL subscriptions:
- WebSocket server setup
- Redis PubSub integration
- Filtered subscriptions
- Client examples
- Production considerations

### 6. apollo-studio.yaml
Apollo Studio integration for:
- Schema management
- Usage reporting
- Performance monitoring
- Error tracking
- CI/CD integration

## Usage

Load this skill in your project:

```bash
# Reference in your agent/AI configuration
@load skills/api/graphql
```

Or include specific templates:

```bash
# Copy schema template
cp skills/api/graphql/templates/graphql-schema.graphql src/schema.graphql

# Copy resolver patterns
cp skills/api/graphql/templates/resolver-patterns.ts src/resolvers/

# Copy DataLoader implementation
cp skills/api/graphql/templates/dataloader-implementation.ts src/dataloaders/
```

## Quick Start

1. **Read SKILL.md** - Start with Level 1 (Quick Reference)
2. **Review templates** - Examine schema and resolver patterns
3. **Implement incrementally** - Start with basic setup, add features
4. **Configure monitoring** - Set up Apollo Studio
5. **Deploy to production** - Use health checks and observability

## Key Features

- ✅ Modern GraphQL frameworks (Apollo Server, GraphQL Yoga)
- ✅ Apollo Federation v2 with subgraphs
- ✅ DataLoader patterns for N+1 prevention
- ✅ Real-time subscriptions with WebSocket
- ✅ Comprehensive error handling
- ✅ Production deployment patterns
- ✅ Apollo Studio integration
- ✅ TypeScript examples throughout

## Prerequisites

- Node.js 18+ (for Apollo Server v4)
- Redis (for subscriptions and caching)
- Basic GraphQL knowledge
- TypeScript familiarity

## Related Skills

- `skills/api/rest-api` - REST API design patterns
- `skills/security/authentication` - Auth implementation
- `skills/database/query-optimization` - Database performance
- `skills/testing/integration-testing` - API testing strategies

## Support

For issues or questions:
1. Review Level 2 Implementation Guide in SKILL.md
2. Check template comments for inline documentation
3. Consult official Apollo/GraphQL documentation
4. Review production considerations in subscription-server.ts

---

**Created**: 2025-10-17
**Version**: 1.0.0
**Category**: API Development
**Difficulty**: Intermediate
**Estimated Time**: 45 minutes
