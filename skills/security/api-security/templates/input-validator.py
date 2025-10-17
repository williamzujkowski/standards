"""
Pydantic Input Validation Models for API Security
NIST Controls: SI-10 (Information Input Validation)
"""

from pydantic import BaseModel, Field, EmailStr, validator, root_validator
from typing import Optional, List
from datetime import datetime
import re

class CreateUserRequest(BaseModel):
    """User creation with comprehensive validation"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30, regex=r'^[a-zA-Z0-9_-]+$')
    password: str = Field(..., min_length=12, max_length=128)
    age: Optional[int] = Field(None, ge=0, le=150)
    roles: List[str] = Field(default_factory=list, max_items=10)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username must be alphanumeric with hyphens/underscores')
        return v

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 12:
            raise ValueError('Password must be at least 12 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain special character')
        return v

    @validator('roles')
    def validate_roles(cls, v):
        allowed = {'user', 'admin', 'moderator'}
        if not set(v).issubset(allowed):
            raise ValueError(f'Invalid roles. Allowed: {allowed}')
        return v

    class Config:
        extra = 'forbid'

class DateRangeQuery(BaseModel):
    """Date range with validation"""
    start_date: datetime
    end_date: datetime

    @root_validator
    def check_date_range(cls, values):
        start = values.get('start_date')
        end = values.get('end_date')
        if start and end and start >= end:
            raise ValueError('start_date must be before end_date')
        return values

class PaginationParams(BaseModel):
    """Pagination with sensible limits"""
    page: int = Field(1, ge=1, le=10000)
    per_page: int = Field(20, ge=1, le=100)

    @property
    def offset(self):
        return (self.page - 1) * self.per_page

class FileUploadRequest(BaseModel):
    """File upload validation"""
    filename: str = Field(..., max_length=255)
    content_type: str
    size_bytes: int = Field(..., ge=1, le=10485760)  # Max 10MB

    @validator('content_type')
    def validate_content_type(cls, v):
        allowed = {'image/jpeg', 'image/png', 'application/pdf'}
        if v not in allowed:
            raise ValueError(f'Content type not allowed. Allowed: {allowed}')
        return v

    @validator('filename')
    def sanitize_filename(cls, v):
        # Remove path traversal attempts
        v = v.replace('..', '').replace('/', '').replace('\\', '')
        if not re.match(r'^[a-zA-Z0-9._-]+$', v):
            raise ValueError('Invalid filename characters')
        return v
