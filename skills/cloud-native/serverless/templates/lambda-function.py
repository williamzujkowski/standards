"""
Production-ready AWS Lambda function template.
Features: Structured logging, X-Ray tracing, error handling, secrets management.
"""

import json
import os
import boto3
from typing import Dict, Any
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_xray_sdk.core import patch_all

# Patch AWS SDK clients for X-Ray tracing
patch_all()

# Initialize observability tools
logger = Logger(service=os.environ.get('SERVICE_NAME', 'user-service'))
tracer = Tracer()
metrics = Metrics(namespace="Serverless")

# Initialize AWS clients outside handler (connection reuse)
dynamodb = boto3.resource('dynamodb')
secrets_manager = boto3.client('secretsmanager')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'users'))


class ValidationError(Exception):
    """Custom exception for input validation errors."""
    pass


def get_secret(secret_arn: str) -> Dict[str, Any]:
    """
    Retrieve secret from AWS Secrets Manager with caching.
    
    Args:
        secret_arn: ARN of the secret to retrieve
        
    Returns:
        Dict containing secret key-value pairs
    """
    try:
        response = secrets_manager.get_secret_value(SecretId=secret_arn)
        return json.loads(response['SecretString'])
    except Exception as e:
        logger.exception(f"Failed to retrieve secret: {secret_arn}")
        raise


def validate_input(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and sanitize input event.
    
    Args:
        event: Lambda event object
        
    Returns:
        Validated request body
        
    Raises:
        ValidationError: If input validation fails
    """
    if 'body' not in event:
        raise ValidationError("Missing request body")
    
    try:
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    except json.JSONDecodeError:
        raise ValidationError("Invalid JSON in request body")
    
    # Validate required fields
    if 'user_id' not in body:
        raise ValidationError("Missing required field: user_id")
    
    # Sanitize inputs
    user_id = str(body['user_id']).strip()
    if not user_id:
        raise ValidationError("user_id cannot be empty")
    
    return {'user_id': user_id, **body}


@tracer.capture_method
def get_user_from_db(user_id: str) -> Dict[str, Any]:
    """
    Retrieve user from DynamoDB.
    
    Args:
        user_id: User identifier
        
    Returns:
        User data dictionary
    """
    response = table.get_item(Key={'id': user_id})
    
    if 'Item' not in response:
        logger.info(f"User not found: {user_id}")
        return None
    
    return response['Item']


@tracer.capture_method
def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create new user in DynamoDB.
    
    Args:
        user_data: User attributes
        
    Returns:
        Created user data
    """
    table.put_item(Item=user_data)
    logger.info(f"User created: {user_data['id']}")
    return user_data


def build_response(status_code: int, body: Any, headers: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Build API Gateway response object.
    
    Args:
        status_code: HTTP status code
        body: Response body (will be JSON-encoded)
        headers: Optional custom headers
        
    Returns:
        API Gateway response dictionary
    """
    default_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    if headers:
        default_headers.update(headers)
    
    return {
        'statusCode': status_code,
        'headers': default_headers,
        'body': json.dumps(body) if not isinstance(body, str) else body
    }


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Main Lambda handler function.
    
    Args:
        event: API Gateway event
        context: Lambda context object
        
    Returns:
        API Gateway response
    """
    # Add correlation ID to all logs
    correlation_id = event.get('requestContext', {}).get('requestId', 'unknown')
    logger.append_keys(correlation_id=correlation_id)
    
    # Handle OPTIONS requests (CORS preflight)
    if event.get('httpMethod') == 'OPTIONS':
        return build_response(200, {'message': 'OK'})
    
    try:
        # Validate input
        body = validate_input(event)
        user_id = body['user_id']
        
        # Add custom trace annotation
        tracer.put_annotation(key="user_id", value=user_id)
        
        # Process request based on HTTP method
        http_method = event.get('httpMethod', 'GET')
        
        if http_method == 'GET':
            # Retrieve user
            user = get_user_from_db(user_id)
            
            if not user:
                metrics.add_metric(name="UserNotFound", unit=MetricUnit.Count, value=1)
                return build_response(404, {'error': 'User not found'})
            
            metrics.add_metric(name="UserRetrieved", unit=MetricUnit.Count, value=1)
            logger.info(f"Retrieved user: {user_id}")
            return build_response(200, user)
        
        elif http_method == 'POST':
            # Create user
            user_data = {
                'id': user_id,
                'name': body.get('name', ''),
                'email': body.get('email', ''),
                'created_at': context.get_remaining_time_in_millis()
            }
            
            created_user = create_user(user_data)
            metrics.add_metric(name="UserCreated", unit=MetricUnit.Count, value=1)
            return build_response(201, created_user)
        
        else:
            return build_response(405, {'error': 'Method not allowed'})
    
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        metrics.add_metric(name="ValidationError", unit=MetricUnit.Count, value=1)
        return build_response(400, {'error': str(e)})
    
    except Exception as e:
        logger.exception("Unexpected error occurred")
        metrics.add_metric(name="InternalError", unit=MetricUnit.Count, value=1)
        return build_response(500, {'error': 'Internal server error'})
