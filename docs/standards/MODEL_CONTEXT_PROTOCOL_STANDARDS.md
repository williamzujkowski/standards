# Model Context Protocol Standards

**Version:** 1.0.0
**Last Updated:** 2025-07-02
**Status:** Active
**Standard Code:** MCP

## 🎯 Micro Summary (100 tokens)

MCP enables AI assistants to interact with external services through:
- **Servers**: Expose tools/resources via standard protocol
- **Clients**: Connect to servers with retry/caching
- **Tools**: Executable functions with validated parameters
- **Resources**: Data providers with URI-based access
- **Security**: JWT auth + input validation + privacy filters

Key pattern: `Server → Transport → Client → Tool/Resource → Response`

---

## Table of Contents

1. [Overview](#overview)
2. [Core Principles](#core-principles)
3. [MCP Architecture Standards](#mcp-architecture-standards)
4. [Server Implementation Standards](#server-implementation-standards)
5. [Client Integration Standards](#client-integration-standards)
6. [Tool Development Standards](#tool-development-standards)
7. [Resource Management Standards](#resource-management-standards)
8. [Security and Privacy Standards](#security-and-privacy-standards)
9. [Testing and Validation](#testing--validation)
10. [Performance Guidelines](#performance-guidelines)
11. [Implementation Checklist](#implementation-checklist)

---

## Overview

The Model Context Protocol (MCP) is an open standard that enables seamless integration between AI assistants and external data sources, tools, and services. This standard defines best practices for implementing MCP servers, clients, and tools within the comprehensive standards framework.

### Quick Start

```bash
# Install MCP SDK
npm install @modelcontextprotocol/sdk

# Create basic server
mcp-server init my-server

# Test connection
mcp-client test --server localhost:3000
```

### When to Use This Standard

- Building MCP servers to expose data or functionality to AI assistants
- Integrating MCP clients into applications
- Developing tools that AI assistants can invoke
- Creating resource providers for AI context
- Implementing secure AI-to-service communications

### Prerequisites

- Understanding of [CLAUDE.md](../core/CLAUDE.md) for LLM optimization
- Familiarity with [CS:api](CODING_STANDARDS.md#14-api-design) standards
- Knowledge of [SEC:auth](MODERN_SECURITY_STANDARDS.md#api-authentication-and-authorization) patterns
- Background in event-driven architectures ([EVT:*](EVENT_DRIVEN_STANDARDS.md))

### 🚀 Quick Reference

| Component | Key Requirements | Priority |
|-----------|------------------|----------|
| Server | Base class, error handling, transport | Critical |
| Client | Retry logic, caching, connection pool | High |
| Tools | Parameter validation, execution monitoring | High |
| Resources | URI validation, caching strategy | Medium |
| Security | JWT auth, input validation, privacy filters | Critical |

### 📌 Common MCP Patterns

```python
# Quick Server Setup
server = MCPServer("my-server", StdioTransport())
server.register_tool(MyTool())
await server.start()

# Quick Client Connection
client = StandardMCPClient({})
await client.connect("server-uri")
result = await client.callTool("tool-name", params)

# Quick Tool Definition
class MyTool(MCPTool):
    def __init__(self):
        super().__init__("my_tool", "Tool description")
        self.add_parameter(MCPToolParameter(
            name="param", type="string", description="Param desc"
        ))
```

---

## Core Principles

### 1. Context Efficiency

**Summary:** Minimize token usage while preserving essential context
**Priority:** Critical
**Token Estimate:** ~200

Optimize for minimal token usage while maintaining comprehensive context:

```python
# Good: Efficient context structure
class MCPContext:
    """Minimal context with progressive disclosure."""

    def __init__(self):
        self.summary = {}  # Quick access data
        self.detailed = {}  # Load on demand
        self.metadata = {
            "token_estimate": 0,
            "priority": "high",
            "cacheable": True
        }

    def get_context(self, level="summary"):
        """Return context at requested detail level."""
        if level == "summary":
            return self.summary
        return {**self.summary, **self.detailed}
```

### 2. Standardized Communication

**Summary:** Use consistent message formats across all MCP interactions
**Priority:** Critical
**Token Estimate:** ~150

Follow consistent patterns for all MCP communications:

```typescript
// Standard message structure
interface MCPMessage {
  id: string;
  method: string;
  params?: any;
  meta: {
    timestamp: number;
    version: string;
    tokenEstimate?: number;
  };
}

// Standard response structure
interface MCPResponse {
  id: string;
  result?: any;
  error?: MCPError;
  meta: {
    processingTime: number;
    tokensUsed?: number;
  };
}
```

### 3. Progressive Loading

**Summary:** Load data incrementally based on detail level requirements
**Priority:** High
**Token Estimate:** ~150

Implement progressive loading patterns aligned with [KM:progressive-disclosure](KNOWLEDGE_MANAGEMENT_STANDARDS.md#progressive-disclosure-system):

```python
class ProgressiveResource:
    """Resource with progressive loading capabilities."""

    def __init__(self, resource_id: str):
        self.id = resource_id
        self.levels = ["micro", "summary", "detailed", "complete"]

    async def load(self, level: str = "summary"):
        """Load resource at specified detail level."""
        if level not in self.levels:
            raise ValueError(f"Invalid level: {level}")

        # Load only what's needed
        data = await self._fetch_data(level)
        return self._optimize_tokens(data, level)
```

---

## MCP Architecture Standards

**Section Summary:** Define modular server structure, manifest requirements, and transport options
**Tokens:** ~1500 | **Priority:** High

### [REQUIRED] Server Architecture

MCP servers must follow a modular, extensible architecture:

```
mcp-server/
├── src/
│   ├── server.py           # Main server implementation
│   ├── handlers/           # Request handlers
│   │   ├── tools.py       # Tool execution
│   │   ├── resources.py   # Resource management
│   │   └── prompts.py     # Prompt handling
│   ├── security/          # Security implementations
│   │   ├── auth.py        # Authentication
│   │   └── validation.py  # Input validation
│   ├── utils/             # Utilities
│   └── config/            # Configuration
├── tests/                 # Test suite (85%+ coverage)
├── docs/                  # Documentation
└── mcp.json              # MCP manifest
```

### [REQUIRED] MCP Manifest

Every MCP server must include a manifest:

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "description": "MCP server for X functionality",
  "author": "Your Name",
  "license": "MIT",
  "capabilities": {
    "tools": true,
    "resources": true,
    "prompts": false,
    "sampling": false
  },
  "requirements": {
    "mcp": ">=1.0.0",
    "python": ">=3.9"
  },
  "security": {
    "authentication": "bearer",
    "rateLimit": {
      "requests": 1000,
      "window": "1h"
    }
  }
}
```

### [RECOMMENDED] Transport Layer

Implement multiple transport options:

```python
from abc import ABC, abstractmethod

class MCPTransport(ABC):
    """Base transport interface."""

    @abstractmethod
    async def send(self, message: dict) -> dict:
        """Send message and await response."""
        pass

    @abstractmethod
    async def connect(self) -> None:
        """Establish connection."""
        pass

class StdioTransport(MCPTransport):
    """Standard I/O transport for local communication."""

    async def send(self, message: dict) -> dict:
        # Implementation for stdio
        pass

class HTTPTransport(MCPTransport):
    """HTTP/WebSocket transport for remote communication."""

    def __init__(self, endpoint: str, auth_token: str = None):
        self.endpoint = endpoint
        self.auth_token = auth_token

    async def send(self, message: dict) -> dict:
        # Implementation for HTTP
        pass
```

---

## Server Implementation Standards

**Section Summary:** Base server class, error handling patterns, and implementation examples
**Tokens:** ~2500 | **Priority:** High

### [REQUIRED] Base Server Class

All MCP servers must extend a common base class:

```python
from typing import Dict, List, Optional
import asyncio
import logging

class MCPServer:
    """Base MCP server implementation."""

    def __init__(self, name: str, transport: MCPTransport):
        self.name = name
        self.transport = transport
        self.handlers = {}
        self.resources = {}
        self.tools = {}
        self.logger = logging.getLogger(name)

        # Register standard handlers
        self._register_standard_handlers()

    def _register_standard_handlers(self):
        """Register required MCP handlers."""
        self.register_handler("initialize", self._handle_initialize)
        self.register_handler("list_tools", self._handle_list_tools)
        self.register_handler("list_resources", self._handle_list_resources)
        self.register_handler("call_tool", self._handle_call_tool)
        self.register_handler("read_resource", self._handle_read_resource)

    async def start(self):
        """Start the MCP server."""
        self.logger.info(f"Starting MCP server: {self.name}")
        await self.transport.connect()
        await self._run_event_loop()

    def register_tool(self, tool: 'MCPTool'):
        """Register a tool with the server."""
        # Validate tool
        tool.validate()
        self.tools[tool.name] = tool
        self.logger.info(f"Registered tool: {tool.name}")

    def register_resource(self, resource: 'MCPResource'):
        """Register a resource with the server."""
        # Validate resource
        resource.validate()
        self.resources[resource.uri] = resource
        self.logger.info(f"Registered resource: {resource.uri}")
```

### [REQUIRED] Error Handling

Implement comprehensive error handling following [CS:error-handling](CODING_STANDARDS.md#6-error-handling):

```python
class MCPError(Exception):
    """Base MCP error class."""

    def __init__(self, code: int, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details
        }

class MCPValidationError(MCPError):
    """Validation error for invalid requests."""

    def __init__(self, message: str, field: str = None):
        details = {"field": field} if field else {}
        super().__init__(400, message, details)

class MCPAuthenticationError(MCPError):
    """Authentication error."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(401, message)

class MCPRateLimitError(MCPError):
    """Rate limit exceeded error."""

    def __init__(self, retry_after: int):
        super().__init__(429, "Rate limit exceeded", {"retry_after": retry_after})
```

---

## Client Integration Standards

**Section Summary:** Client interface, connection management, and intelligent caching
**Tokens:** ~2000 | **Priority:** High

### [REQUIRED] Client Implementation

MCP clients must implement a standard interface:

```typescript
interface MCPClient {
  // Connection management
  connect(serverUri: string, options?: ConnectionOptions): Promise<void>;
  disconnect(): Promise<void>;
  isConnected(): boolean;

  // Tool operations
  listTools(): Promise<Tool[]>;
  callTool(name: string, params: any): Promise<any>;

  // Resource operations
  listResources(): Promise<Resource[]>;
  readResource(uri: string): Promise<any>;
  subscribeToResource(uri: string, callback: (data: any) => void): Subscription;

  // Event handling
  on(event: string, handler: Function): void;
  off(event: string, handler: Function): void;
}

class StandardMCPClient implements MCPClient {
  private connection: MCPConnection;
  private subscriptions: Map<string, Subscription>;

  constructor(private config: ClientConfig) {
    this.subscriptions = new Map();
  }

  async connect(serverUri: string, options?: ConnectionOptions): Promise<void> {
    // Implement connection with retry logic
    const maxRetries = options?.maxRetries || 3;
    let attempt = 0;

    while (attempt < maxRetries) {
      try {
        this.connection = await this.createConnection(serverUri, options);
        await this.initialize();
        break;
      } catch (error) {
        attempt++;
        if (attempt === maxRetries) throw error;
        await this.delay(Math.pow(2, attempt) * 1000); // Exponential backoff
      }
    }
  }
}
```

### [RECOMMENDED] Client Caching

Implement intelligent caching aligned with [CLAUDE.md cache management](../core/CLAUDE.md#cache-management):

```python
from functools import lru_cache
from datetime import datetime, timedelta

class MCPClientCache:
    """Intelligent caching for MCP clients."""

    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl
        self.cache = {}
        self.metadata = {}

    def get(self, key: str) -> Optional[any]:
        """Get cached value if not expired."""
        if key in self.cache:
            meta = self.metadata[key]
            if datetime.now() < meta["expires"]:
                meta["hits"] += 1
                return self.cache[key]
            else:
                # Expired, remove
                del self.cache[key]
                del self.metadata[key]
        return None

    def set(self, key: str, value: any, ttl: int = None):
        """Cache value with TTL."""
        ttl = ttl or self.default_ttl
        self.cache[key] = value
        self.metadata[key] = {
            "expires": datetime.now() + timedelta(seconds=ttl),
            "hits": 0,
            "size": self._estimate_size(value)
        }

    @lru_cache(maxsize=100)
    def _estimate_size(self, value: any) -> int:
        """Estimate memory size of cached value."""
        # Implementation for size estimation
        pass
```

---

## Tool Development Standards

**Section Summary:** Tool structure, parameter validation, and concrete examples
**Tokens:** ~2200 | **Priority:** High

### [REQUIRED] Tool Structure

All MCP tools must follow this structure:

```python
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class MCPToolParameter(BaseModel):
    """Tool parameter definition."""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None
    enum: List[str] = None

class MCPTool:
    """Base class for MCP tools."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.parameters: List[MCPToolParameter] = []
        self._validator = None

    def add_parameter(self, param: MCPToolParameter):
        """Add parameter to tool."""
        self.parameters.append(param)
        self._rebuild_validator()

    def validate(self):
        """Validate tool configuration."""
        if not self.name:
            raise ValueError("Tool name is required")
        if not self.description:
            raise ValueError("Tool description is required")
        # Additional validation

    async def execute(self, params: Dict[str, Any]) -> Any:
        """Execute the tool with given parameters."""
        # Validate parameters
        validated = self._validate_params(params)

        # Execute with monitoring
        start_time = time.time()
        try:
            result = await self._execute_impl(validated)
            self._record_success(time.time() - start_time)
            return result
        except Exception as e:
            self._record_failure(time.time() - start_time, e)
            raise

    async def _execute_impl(self, params: Dict[str, Any]) -> Any:
        """Actual tool implementation - override in subclasses."""
        raise NotImplementedError
```

### [REQUIRED] Tool Examples

Provide concrete tool implementations:

```python
class DatabaseQueryTool(MCPTool):
    """Tool for executing database queries."""

    def __init__(self, connection_string: str):
        super().__init__(
            name="database_query",
            description="Execute SQL queries with safety checks"
        )
        self.connection_string = connection_string

        # Define parameters
        self.add_parameter(MCPToolParameter(
            name="query",
            type="string",
            description="SQL query to execute"
        ))
        self.add_parameter(MCPToolParameter(
            name="params",
            type="object",
            description="Query parameters for safe execution",
            required=False,
            default={}
        ))

    async def _execute_impl(self, params: Dict[str, Any]) -> Any:
        """Execute database query safely."""
        query = params["query"]
        query_params = params.get("params", {})

        # Validate query (prevent SQL injection)
        if not self._is_safe_query(query):
            raise MCPValidationError("Unsafe query detected")

        # Execute with connection pooling
        async with self._get_connection() as conn:
            result = await conn.fetch(query, **query_params)
            return [dict(row) for row in result]

    def _is_safe_query(self, query: str) -> bool:
        """Check if query is safe to execute."""
        # Implement safety checks
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER"]
        query_upper = query.upper()
        return not any(kw in query_upper for kw in dangerous_keywords)
```

---

## Resource Management Standards

**Section Summary:** Resource contracts, caching strategies, and common resource types
**Tokens:** ~1800 | **Priority:** Medium

### [REQUIRED] Resource Definition

Define resources with clear contracts:

```python
class MCPResource:
    """Base class for MCP resources."""

    def __init__(self, uri: str, name: str, mime_type: str = "application/json"):
        self.uri = uri
        self.name = name
        self.mime_type = mime_type
        self.metadata = {
            "created": datetime.now(),
            "version": "1.0.0",
            "cacheable": True,
            "ttl": 3600
        }

    def validate(self):
        """Validate resource configuration."""
        if not self.uri:
            raise ValueError("Resource URI is required")
        if not self.uri.startswith(("file://", "http://", "https://", "data:")):
            raise ValueError("Invalid URI scheme")

    async def read(self, options: Dict[str, Any] = None) -> Any:
        """Read resource data."""
        # Check cache first
        cached = await self._check_cache()
        if cached:
            return cached

        # Load data
        data = await self._load_data(options)

        # Cache if appropriate
        if self.metadata.get("cacheable"):
            await self._cache_data(data)

        return data

    async def subscribe(self, callback: Callable) -> 'Subscription':
        """Subscribe to resource changes."""
        return Subscription(self, callback)
```

### [RECOMMENDED] Resource Types

Implement common resource types:

```python
class FileResource(MCPResource):
    """File-based resource."""

    def __init__(self, file_path: str):
        uri = f"file://{os.path.abspath(file_path)}"
        name = os.path.basename(file_path)
        mime_type = self._detect_mime_type(file_path)
        super().__init__(uri, name, mime_type)
        self.file_path = file_path

    async def _load_data(self, options: Dict[str, Any] = None) -> Any:
        """Load file data."""
        async with aiofiles.open(self.file_path, 'r') as f:
            content = await f.read()

        if self.mime_type == "application/json":
            return json.loads(content)
        return content

class APIResource(MCPResource):
    """API-based resource."""

    def __init__(self, endpoint: str, auth_token: str = None):
        super().__init__(endpoint, endpoint.split('/')[-1])
        self.endpoint = endpoint
        self.auth_token = auth_token

    async def _load_data(self, options: Dict[str, Any] = None) -> Any:
        """Load data from API."""
        headers = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        async with aiohttp.ClientSession() as session:
            async with session.get(self.endpoint, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
```

---

## Security and Privacy Standards

**Section Summary:** Authentication, input validation, and privacy controls
**Tokens:** ~2500 | **Priority:** Critical

### [REQUIRED] Authentication

Implement authentication following [SEC:auth](MODERN_SECURITY_STANDARDS.md#api-authentication-and-authorization):

```python
from abc import ABC, abstractmethod
import jwt
import secrets

class MCPAuthenticator(ABC):
    """Base authenticator for MCP servers."""

    @abstractmethod
    async def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Authenticate request."""
        pass

    @abstractmethod
    async def get_permissions(self, identity: str) -> List[str]:
        """Get permissions for authenticated identity."""
        pass

class JWTAuthenticator(MCPAuthenticator):
    """JWT-based authentication."""

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Validate JWT token."""
        token = credentials.get("token")
        if not token:
            return False

        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            # Additional validation
            return self._validate_claims(payload)
        except jwt.InvalidTokenError:
            return False

    def _validate_claims(self, payload: dict) -> bool:
        """Validate JWT claims."""
        # Check expiration
        if "exp" in payload and payload["exp"] < time.time():
            return False

        # Check required claims
        required_claims = ["sub", "iat"]
        return all(claim in payload for claim in required_claims)
```

### [REQUIRED] Input Validation

Validate all inputs following [SEC:validation](MODERN_SECURITY_STANDARDS.md#4-api-security):

```python
class MCPValidator:
    """Input validation for MCP requests."""

    @staticmethod
    def validate_tool_params(tool: MCPTool, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate tool parameters."""
        validated = {}

        for param in tool.parameters:
            value = params.get(param.name)

            # Check required
            if param.required and value is None:
                raise MCPValidationError(
                    f"Required parameter missing: {param.name}",
                    field=param.name
                )

            # Type validation
            if value is not None:
                validated[param.name] = MCPValidator._validate_type(
                    value, param.type, param.name
                )

            # Enum validation
            if param.enum and value not in param.enum:
                raise MCPValidationError(
                    f"Invalid value for {param.name}. Must be one of: {param.enum}",
                    field=param.name
                )

        return validated

    @staticmethod
    def _validate_type(value: Any, expected_type: str, field: str) -> Any:
        """Validate parameter type."""
        type_map = {
            "string": str,
            "number": (int, float),
            "boolean": bool,
            "object": dict,
            "array": list
        }

        expected = type_map.get(expected_type)
        if expected and not isinstance(value, expected):
            raise MCPValidationError(
                f"Invalid type for {field}. Expected {expected_type}",
                field=field
            )

        # Additional validation for strings
        if expected_type == "string" and isinstance(value, str):
            # Prevent injection attacks
            if any(char in value for char in ["<", ">", "&", '"', "'"]):
                value = html.escape(value)

        return value
```

### [RECOMMENDED] Privacy Controls

Implement privacy controls for sensitive data:

```python
class MCPPrivacyFilter:
    """Filter sensitive data from MCP responses."""

    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = rules
        self.redaction_patterns = self._compile_patterns()

    def filter(self, data: Any) -> Any:
        """Apply privacy filters to data."""
        if isinstance(data, dict):
            return {k: self._filter_value(k, v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.filter(item) for item in data]
        else:
            return self._filter_value("", data)

    def _filter_value(self, key: str, value: Any) -> Any:
        """Filter individual value."""
        # Check rules
        for rule in self.rules:
            if self._matches_rule(key, value, rule):
                return self._apply_rule(value, rule)

        # Recursively filter nested structures
        if isinstance(value, (dict, list)):
            return self.filter(value)

        return value

    def _apply_rule(self, value: Any, rule: Dict[str, Any]) -> Any:
        """Apply privacy rule to value."""
        action = rule.get("action", "redact")

        if action == "redact":
            return "[REDACTED]"
        elif action == "hash":
            return hashlib.sha256(str(value).encode()).hexdigest()[:8]
        elif action == "mask":
            if isinstance(value, str):
                return value[:2] + "*" * (len(value) - 4) + value[-2:]
            return "[MASKED]"

        return value
```

---

## Testing and Validation

**Section Summary:** Test patterns, integration tests, and performance benchmarks
**Tokens:** ~2000 | **Priority:** High

### [REQUIRED] Test Suite Structure

Follow [TS:*](TESTING_STANDARDS.md) with MCP-specific tests:

```python
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

class TestMCPServer:
    """Test suite for MCP server."""

    @pytest.fixture
    async def server(self):
        """Create test server instance."""
        transport = Mock(spec=MCPTransport)
        server = MCPServer("test-server", transport)
        yield server
        # Cleanup

    @pytest.fixture
    async def authenticated_request(self):
        """Create authenticated request."""
        return {
            "id": "test-123",
            "method": "call_tool",
            "params": {
                "name": "test_tool",
                "arguments": {}
            },
            "auth": {
                "token": "valid-jwt-token"
            }
        }

    async def test_server_initialization(self, server):
        """Test server initializes correctly."""
        assert server.name == "test-server"
        assert len(server.handlers) > 0
        assert "initialize" in server.handlers
        assert "list_tools" in server.handlers

    async def test_tool_registration(self, server):
        """Test tool registration."""
        tool = Mock(spec=MCPTool)
        tool.name = "test_tool"
        tool.validate = Mock()

        server.register_tool(tool)

        assert "test_tool" in server.tools
        tool.validate.assert_called_once()

    async def test_authentication_required(self, server):
        """Test authentication is enforced."""
        # Configure server to require auth
        server.authenticator = Mock(spec=MCPAuthenticator)
        server.authenticator.authenticate = AsyncMock(return_value=False)

        request = {
            "id": "test-123",
            "method": "call_tool",
            "params": {}
        }

        response = await server.handle_request(request)
        assert response["error"]["code"] == 401
```

### [REQUIRED] Integration Tests

Test MCP server/client integration:

```python
class TestMCPIntegration:
    """Integration tests for MCP."""

    @pytest.fixture
    async def running_server(self):
        """Start actual MCP server."""
        server = await create_test_server()
        yield server
        await server.shutdown()

    @pytest.fixture
    async def client(self, running_server):
        """Create connected client."""
        client = StandardMCPClient({})
        await client.connect(running_server.uri)
        yield client
        await client.disconnect()

    async def test_end_to_end_tool_call(self, client):
        """Test complete tool call flow."""
        # List tools
        tools = await client.listTools()
        assert len(tools) > 0

        # Call tool
        result = await client.callTool("echo", {"message": "Hello MCP"})
        assert result == {"echo": "Hello MCP"}

    async def test_resource_subscription(self, client):
        """Test resource subscription."""
        updates = []

        subscription = await client.subscribeToResource(
            "data://test/counter",
            lambda data: updates.append(data)
        )

        # Wait for updates
        await asyncio.sleep(2)

        assert len(updates) > 0
        await subscription.unsubscribe()
```

### [RECOMMENDED] Performance Tests

Benchmark MCP operations:

```python
import time
import statistics

class TestMCPPerformance:
    """Performance benchmarks for MCP."""

    @pytest.mark.benchmark
    async def test_tool_call_performance(self, client, benchmark_tool):
        """Benchmark tool call performance."""
        timings = []

        for _ in range(100):
            start = time.time()
            await client.callTool(benchmark_tool, {"n": 1000})
            timings.append(time.time() - start)

        avg_time = statistics.mean(timings)
        p95_time = statistics.quantiles(timings, n=20)[18]  # 95th percentile

        assert avg_time < 0.1  # Average under 100ms
        assert p95_time < 0.2  # 95th percentile under 200ms

    @pytest.mark.benchmark
    async def test_concurrent_operations(self, client):
        """Test concurrent operation handling."""
        async def call_tool(n):
            return await client.callTool("compute", {"n": n})

        start = time.time()
        results = await asyncio.gather(*[
            call_tool(i) for i in range(50)
        ])
        total_time = time.time() - start

        assert len(results) == 50
        assert total_time < 5.0  # All complete within 5 seconds
```

---

## Performance Guidelines

**Section Summary:** Performance targets and optimization strategies
**Tokens:** ~1200 | **Priority:** Medium

### Performance Targets

| Operation                | Target | Maximum |
| ------------------------ | ------ | ------- |
| Tool call latency        | <50ms  | 200ms   |
| Resource read            | <100ms | 500ms   |
| Connection establishment | <500ms | 2s      |
| Message parsing          | <5ms   | 20ms    |
| Token estimation         | <1ms   | 5ms     |

### Optimization Strategies

1. **Connection Pooling**
   ```python
   class MCPConnectionPool:
       """Reusable connection pool."""

       def __init__(self, max_connections: int = 10):
           self.pool = asyncio.Queue(maxsize=max_connections)
           self.semaphore = asyncio.Semaphore(max_connections)
   ```

2. **Message Batching**
   ```python
   class MCPBatcher:
       """Batch multiple operations."""

       async def batch_call_tools(self, calls: List[Dict]) -> List[Any]:
           """Execute multiple tool calls efficiently."""
           return await asyncio.gather(*[
               self._call_tool(**call) for call in calls
           ])
   ```

3. **Resource Caching**
   - Cache frequently accessed resources
   - Implement cache warming on startup
   - Use cache invalidation strategies

---

## Implementation Checklist

### Phase 1: Foundation (Week 1)
- [ ] Set up MCP server structure
- [ ] Implement base server class
- [ ] Add authentication mechanism
- [ ] Create first tool implementation
- [ ] Write basic test suite

### Phase 2: Core Features (Week 2-3)
- [ ] Implement resource management
- [ ] Add multiple transport options
- [ ] Create client library
- [ ] Implement caching layer
- [ ] Add comprehensive error handling
- [ ] Reach 85% test coverage

### Phase 3: Advanced Features (Week 4+)
- [ ] Add resource subscriptions
- [ ] Implement privacy filters
- [ ] Create performance monitoring
- [ ] Add tool composition
- [ ] Build admin interface
- [ ] Complete documentation

### Validation Checklist
- [ ] All [REQUIRED] standards implemented
- [ ] Security measures in place
- [ ] Test coverage ≥85%
- [ ] Performance targets met
- [ ] Documentation complete
- [ ] Examples provided

---

## References

- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [CLAUDE.md](../core/CLAUDE.md) - LLM optimization patterns
- [CODING_STANDARDS.md](CODING_STANDARDS.md) - General coding standards
- [MODERN_SECURITY_STANDARDS.md](MODERN_SECURITY_STANDARDS.md) - Security requirements
- [TESTING_STANDARDS.md](TESTING_STANDARDS.md) - Testing requirements
- [EVENT_DRIVEN_STANDARDS.md](EVENT_DRIVEN_STANDARDS.md) - Event patterns

---

## Appendix: Quick Reference

### MCP Commands
```bash
# Start server
mcp-server start --config mcp.json

# Test connection
mcp-client test --server localhost:3000

# List available tools
mcp-client tools --list

# Call tool
mcp-client call --tool database_query --params '{"query": "SELECT * FROM users"}'
```

### Common Patterns
```python
# Progressive loading
@load MCP:overview  # Quick overview
@load MCP:server-implementation  # Server details
@load MCP:security  # Security specifics

# Task-based loading
@task "build MCP server" → [MCP:server + CS:python + SEC:auth]
@task "integrate MCP client" → [MCP:client + CS:javascript + TS:integration]
```

### Error Codes Quick Reference
| Code | Error | Action |
|------|-------|--------|
| 400 | Validation Error | Check parameters |
| 401 | Authentication Error | Verify credentials |
| 429 | Rate Limit | Retry after delay |
| 500 | Server Error | Check server logs |

---

**Note:** This standard is a living document. Updates and improvements are welcome via pull requests to the [standards repository](https://github.com/williamzujkowski/standards).

## Related Standards

- [Knowledge Management Standards](KNOWLEDGE_MANAGEMENT_STANDARDS.md) - Progressive disclosure patterns
- [Event-Driven Architecture Standards](EVENT_DRIVEN_STANDARDS.md) - Event handling patterns
- [API Standards](CODING_STANDARDS.md#14-api-design) - API design principles
- [Security Standards](MODERN_SECURITY_STANDARDS.md) - Security requirements
