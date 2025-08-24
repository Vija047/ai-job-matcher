"""
Authentication and Security Module
Handles user authentication, JWT tokens, and API security
"""

import os
import jwt
import bcrypt
import redis
from datetime import datetime, timedelta
from functools import wraps
import logging
from typing import Dict, Optional, Any, Union
import hashlib
import secrets
from flask import request, jsonify, current_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthManager:
    """
    Comprehensive authentication and security manager
    Handles JWT tokens, password hashing, session management, and API security
    """
    
    def __init__(self):
        """Initialize the AuthManager with environment-based configuration"""
        # Load configuration from environment variables
        self.jwt_secret = os.getenv('JWT_SECRET_KEY')
        if not self.jwt_secret:
            # Generate a random secret for development (should be set in production)
            self.jwt_secret = secrets.token_urlsafe(32)
            logger.warning("⚠️ JWT_SECRET_KEY not set in environment. Using random secret.")
        
        self.jwt_algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
        self.jwt_expiry = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour
        
        # API Keys configuration
        self.api_keys = {
            'adzuna_app_id': os.getenv('ADZUNA_APP_ID'),
            'adzuna_app_key': os.getenv('ADZUNA_APP_KEY'),
            'rapidapi_key': os.getenv('RAPIDAPI_KEY'),
            'huggingface_api_key': os.getenv('HUGGINGFACE_API_KEY')
        }
        
        # Initialize Redis for session management
        try:
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
            self.redis_client = redis.from_url(redis_url)
            self.redis_client.ping()  # Test connection
            logger.info("✅ Redis connection established")
        except Exception as e:
            logger.warning(f"⚠️ Redis connection failed: {e}. Sessions will be stateless.")
            self.redis_client = None
        
        # Security settings
        self.max_failed_attempts = int(os.getenv('MAX_FAILED_LOGIN_ATTEMPTS', 5))
        self.lockout_duration = int(os.getenv('LOCKOUT_DURATION_MINUTES', 15)) * 60  # seconds
        
        logger.info("🔐 AuthManager initialized successfully")
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        try:
            # Generate salt and hash password
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"❌ Password hashing failed: {e}")
            raise Exception("Password hashing failed")
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            password (str): Plain text password
            hashed_password (str): Hashed password from database
            
        Returns:
            bool: True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"❌ Password verification failed: {e}")
            return False
    
    def generate_jwt_token(self, user_data: Dict[str, Any], expires_in: Optional[int] = None) -> str:
        """
        Generate a JWT token for user authentication
        
        Args:
            user_data (Dict): User information to encode in token
            expires_in (int, optional): Custom expiration time in seconds
            
        Returns:
            str: JWT token
        """
        try:
            expiry = expires_in or self.jwt_expiry
            payload = {
                'user_id': user_data.get('user_id'),
                'email': user_data.get('email'),
                'role': user_data.get('role', 'user'),
                'exp': datetime.utcnow() + timedelta(seconds=expiry),
                'iat': datetime.utcnow(),
                'jti': secrets.token_urlsafe(16)  # JWT ID for token revocation
            }
            
            token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
            logger.info(f"✅ JWT token generated for user: {user_data.get('email')}")
            return token
            
        except Exception as e:
            logger.error(f"❌ JWT token generation failed: {e}")
            raise Exception("Token generation failed")
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token
        
        Args:
            token (str): JWT token to verify
            
        Returns:
            Dict or None: Decoded token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            
            # Check if token is blacklisted
            if self.redis_client and self.is_token_blacklisted(payload.get('jti')):
                logger.warning("⚠️ Attempted use of blacklisted token")
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("⚠️ JWT token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"⚠️ Invalid JWT token: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ JWT token verification failed: {e}")
            return None
    
    def blacklist_token(self, jti: str, exp: int) -> bool:
        """
        Add a token to the blacklist (for logout/revocation)
        
        Args:
            jti (str): JWT ID
            exp (int): Token expiration timestamp
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.redis_client:
            logger.warning("⚠️ Cannot blacklist token: Redis not available")
            return False
        
        try:
            # Calculate TTL based on token expiration
            ttl = exp - int(datetime.utcnow().timestamp())
            if ttl > 0:
                self.redis_client.setex(f"blacklist:{jti}", ttl, "revoked")
                logger.info(f"✅ Token {jti} added to blacklist")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Token blacklisting failed: {e}")
            return False
    
    def is_token_blacklisted(self, jti: str) -> bool:
        """
        Check if a token is blacklisted
        
        Args:
            jti (str): JWT ID
            
        Returns:
            bool: True if blacklisted, False otherwise
        """
        if not self.redis_client:
            return False
        
        try:
            return self.redis_client.exists(f"blacklist:{jti}")
        except Exception as e:
            logger.error(f"❌ Blacklist check failed: {e}")
            return False
    
    def record_failed_attempt(self, identifier: str) -> None:
        """
        Record a failed login attempt
        
        Args:
            identifier (str): Email or IP address
        """
        if not self.redis_client:
            return
        
        try:
            key = f"failed_attempts:{identifier}"
            current_attempts = self.redis_client.get(key)
            attempts = int(current_attempts) + 1 if current_attempts else 1
            
            self.redis_client.setex(key, self.lockout_duration, attempts)
            logger.info(f"🔒 Failed attempt recorded for {identifier}: {attempts}/{self.max_failed_attempts}")
            
        except Exception as e:
            logger.error(f"❌ Failed to record login attempt: {e}")
    
    def is_account_locked(self, identifier: str) -> bool:
        """
        Check if an account is locked due to failed attempts
        
        Args:
            identifier (str): Email or IP address
            
        Returns:
            bool: True if locked, False otherwise
        """
        if not self.redis_client:
            return False
        
        try:
            key = f"failed_attempts:{identifier}"
            attempts = self.redis_client.get(key)
            return int(attempts) >= self.max_failed_attempts if attempts else False
            
        except Exception as e:
            logger.error(f"❌ Account lock check failed: {e}")
            return False
    
    def clear_failed_attempts(self, identifier: str) -> None:
        """
        Clear failed login attempts (on successful login)
        
        Args:
            identifier (str): Email or IP address
        """
        if not self.redis_client:
            return
        
        try:
            self.redis_client.delete(f"failed_attempts:{identifier}")
            logger.info(f"✅ Cleared failed attempts for {identifier}")
            
        except Exception as e:
            logger.error(f"❌ Failed to clear login attempts: {e}")
    
    def generate_api_key(self, user_id: str, key_name: str) -> str:
        """
        Generate a secure API key for a user
        
        Args:
            user_id (str): User identifier
            key_name (str): Name/description of the API key
            
        Returns:
            str: Generated API key
        """
        # Create a unique API key
        key_data = f"{user_id}:{key_name}:{datetime.utcnow().isoformat()}:{secrets.token_urlsafe(32)}"
        api_key = hashlib.sha256(key_data.encode()).hexdigest()
        
        # Store API key metadata in Redis
        if self.redis_client:
            try:
                metadata = {
                    'user_id': user_id,
                    'key_name': key_name,
                    'created_at': datetime.utcnow().isoformat(),
                    'last_used': None,
                    'usage_count': 0
                }
                self.redis_client.hset(f"api_key:{api_key}", mapping=metadata)
                logger.info(f"✅ API key generated for user {user_id}: {key_name}")
            except Exception as e:
                logger.error(f"❌ Failed to store API key metadata: {e}")
        
        return api_key
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """
        Validate an API key and return associated metadata
        
        Args:
            api_key (str): API key to validate
            
        Returns:
            Dict or None: API key metadata if valid, None otherwise
        """
        if not self.redis_client:
            return None
        
        try:
            metadata = self.redis_client.hgetall(f"api_key:{api_key}")
            if metadata:
                # Update usage statistics
                self.redis_client.hincrby(f"api_key:{api_key}", 'usage_count', 1)
                self.redis_client.hset(f"api_key:{api_key}", 'last_used', datetime.utcnow().isoformat())
                
                # Convert bytes to strings (Redis returns bytes)
                return {k.decode(): v.decode() for k, v in metadata.items()}
            return None
            
        except Exception as e:
            logger.error(f"❌ API key validation failed: {e}")
            return None
    
    def get_external_api_key(self, service: str) -> Optional[str]:
        """
        Get external API key for specified service
        
        Args:
            service (str): Service name ('adzuna_app_id', 'adzuna_app_key', etc.)
            
        Returns:
            str or None: API key if available, None otherwise
        """
        key = self.api_keys.get(service)
        if not key:
            logger.warning(f"⚠️ API key not found for service: {service}")
        return key

# Decorator for JWT authentication
def jwt_required(f):
    """
    Decorator to require JWT authentication for routes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid authorization header format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            auth_manager = current_app.config.get('AUTH_MANAGER')
            if not auth_manager:
                return jsonify({'error': 'Authentication service unavailable'}), 500
            
            payload = auth_manager.verify_jwt_token(token)
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            # Add user info to request context
            request.current_user = payload
            
        except Exception as e:
            logger.error(f"❌ JWT authentication failed: {e}")
            return jsonify({'error': 'Authentication failed'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

# Decorator for API key authentication
def api_key_required(f):
    """
    Decorator to require API key authentication for routes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key is missing'}), 401
        
        try:
            auth_manager = current_app.config.get('AUTH_MANAGER')
            if not auth_manager:
                return jsonify({'error': 'Authentication service unavailable'}), 500
            
            key_metadata = auth_manager.validate_api_key(api_key)
            if not key_metadata:
                return jsonify({'error': 'Invalid API key'}), 401
            
            # Add API key info to request context
            request.api_key_metadata = key_metadata
            
        except Exception as e:
            logger.error(f"❌ API key authentication failed: {e}")
            return jsonify({'error': 'Authentication failed'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

# Rate limiting decorator
def rate_limit(max_requests: int = 100, window_seconds: int = 3600):
    """
    Rate limiting decorator
    
    Args:
        max_requests (int): Maximum requests allowed
        window_seconds (int): Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client identifier (IP or user ID)
            client_id = request.remote_addr
            if hasattr(request, 'current_user'):
                client_id = request.current_user.get('user_id', client_id)
            
            auth_manager = current_app.config.get('AUTH_MANAGER')
            if not auth_manager or not auth_manager.redis_client:
                # Skip rate limiting if Redis is not available
                return f(*args, **kwargs)
            
            try:
                key = f"rate_limit:{client_id}:{f.__name__}"
                current_requests = auth_manager.redis_client.get(key)
                
                if current_requests and int(current_requests) >= max_requests:
                    return jsonify({'error': 'Rate limit exceeded'}), 429
                
                # Increment counter
                pipe = auth_manager.redis_client.pipeline()
                pipe.incr(key)
                pipe.expire(key, window_seconds)
                pipe.execute()
                
            except Exception as e:
                logger.error(f"❌ Rate limiting failed: {e}")
                # Continue without rate limiting on error
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

# Initialize global auth manager instance
auth_manager = None

def init_auth_manager():
    """Initialize the global auth manager instance"""
    global auth_manager
    auth_manager = AuthManager()
    return auth_manager

def get_auth_manager() -> AuthManager:
    """Get the global auth manager instance"""
    global auth_manager
    if not auth_manager:
        auth_manager = AuthManager()
    return auth_manager
