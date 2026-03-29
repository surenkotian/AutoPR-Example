"""Enhanced provider utilities with retry logic, error handling, and deterministic behavior."""

import os
import json
import time
import hashlib
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum


class ProviderError(Exception):
    """Base exception for provider-related errors."""
    pass


class RateLimitError(ProviderError):
    """Raised when API rate limit is exceeded."""
    pass


class AuthenticationError(ProviderError):
    """Raised when API authentication fails."""
    pass


class CircuitBreakerOpen(Exception):
    """Raised when circuit breaker is open."""
    pass


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class RetryConfig:
    """Configuration for retry logic."""
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""
    failure_threshold: int = 5
    timeout: float = 60.0
    expected_exception: type = Exception


class CircuitBreaker:
    """Circuit breaker implementation for API resilience."""
    
    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpen("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.config.expected_exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.config.timeout
    
    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN


def calculate_deterministic_seed(prompt: str, provider: str, model: str) -> int:
    """Calculate a deterministic seed based on input parameters."""
    combined = f"{provider}:{model}:{prompt}"
    return int(hashlib.md5(combined.encode()).hexdigest(), 16) % (2**32)


def retry_with_backoff(func, config: RetryConfig = None, *args, **kwargs):
    """Execute function with exponential backoff retry logic."""
    if config is None:
        config = RetryConfig()
    
    last_exception = None
    
    for attempt in range(config.max_retries + 1):
        try:
            return func(*args, **kwargs)
        except (RateLimitError, ProviderError) as e:
            last_exception = e
            
            if attempt == config.max_retries:
                break
            
            delay = min(
                config.base_delay * (config.exponential_base ** attempt),
                config.max_delay
            )
            
            if config.jitter:
                import random
                delay *= (0.5 + random.random() * 0.5)
            
            time.sleep(delay)
    
    raise last_exception


def validate_json_response(text: str) -> Dict[str, Any]:
    """Validate and parse JSON response with error recovery."""
    if not text:
        raise ProviderError("Empty response from provider")
    
    # Try to extract JSON from the response
    try:
        # Remove markdown code blocks if present
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        
        text = text.strip()
        return json.loads(text)
    except json.JSONDecodeError as e:
        # Try to extract JSON from within the text
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        raise ProviderError(f"Invalid JSON response: {e}")


def format_error_message(error: Exception, provider: str, fallback_available: bool = True) -> str:
    """Format error message for user-facing output."""
    if isinstance(error, AuthenticationError):
        return (f"{provider} authentication failed. Please check your API key. "
                "Set AUTOPR_PROVIDER=stub to use offline mode." if fallback_available else "")
    
    elif isinstance(error, RateLimitError):
        return (f"{provider} rate limit exceeded. Please try again later. "
                "Consider using a different provider or stub mode." if fallback_available else "")
    
    elif isinstance(error, CircuitBreakerOpen):
        return (f"{provider} is temporarily unavailable due to repeated failures. "
                "Please try again later or use a different provider." if fallback_available else "")
    
    else:
        return (f"{provider} error: {error}. "
                "Please check your configuration or try a different provider." if fallback_available else str(error))


def get_provider_fallback_message(provider: str) -> str:
    """Get fallback message for when a provider fails."""
    return (
        f"Primary provider ({provider}) failed. AutoPR will attempt to use a fallback provider or stub mode. "
        "You can set AUTOPR_PROVIDER=stub to use offline mode explicitly."
    )