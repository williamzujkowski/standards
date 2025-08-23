# CS:api - API Design Micro Standard (500 tokens max)

## Quick Rules

- REST over HTTP/HTTPS
- Version in URL: `/api/v1/`, `/api/v2/`
- JSON request/response
- Status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Server Error

## URL Patterns

```
GET    /api/v1/users          # List
GET    /api/v1/users/{id}     # Get one
POST   /api/v1/users          # Create
PUT    /api/v1/users/{id}     # Update
DELETE /api/v1/users/{id}     # Delete
```

## Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "field": "email",
    "timestamp": "2025-01-13T10:00:00Z"
  }
}
```

## Pagination

```
GET /api/v1/users?page=2&limit=20
Response headers:
X-Total-Count: 100
X-Page: 2
X-Per-Page: 20
```

## Authentication

- Bearer token in header: `Authorization: Bearer <token>`
- API keys for service-to-service
- Rate limiting: 1000 req/hour per user

## Must Have

✓ Input validation
✓ Error handling
✓ Rate limiting
✓ API documentation (OpenAPI/Swagger)
✓ Health check endpoint: `GET /health`
✓ Request ID tracking
✓ CORS headers for web clients

## Example

```python
@app.post("/api/v1/users")
@validate_input(UserSchema)
@rate_limit("1000/hour")
async def create_user(data: UserCreateRequest) -> UserResponse:
    # Validate → Process → Return
    return UserResponse(id=user.id, email=user.email)
```
