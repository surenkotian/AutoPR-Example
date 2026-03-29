import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LazyProviderProxy:
    def __init__(self):
        self._provider = None

    def _get_provider(self):
        if self._provider is None:
            from .provider_utils import AuthenticationError, ProviderError
            from .providers import create_provider
            try:
                self._provider = create_provider()
            except (AuthenticationError, ProviderError) as e:
                import sys
                import click
                click.echo(f"\n❌ Error: {e}")
                click.echo("🔑 You need to set up your AI provider API key.")
                click.echo("👉 Please run: autopr configure\n")
                sys.exit(1)
        return self._provider

    def __getattr__(self, name):
        provider = self._get_provider()
        attr = getattr(provider, name)
        if callable(attr):
            def _safe_call(*args, **kwargs):
                from .provider_utils import ProviderError, AuthenticationError, RateLimitError
                try:
                    return attr(*args, **kwargs)
                except AuthenticationError as e:
                    import click
                    click.echo(f"\n❌ Authentication failed: {e}")
                    click.echo("🔑 Your API key is invalid or expired.")
                    click.echo("👉 Please run: autopr configure\n")
                    raise SystemExit(1)
                except RateLimitError as e:
                    import click
                    click.echo(f"\n⚠️  Rate limit hit: {e}")
                    click.echo("⏳ Please wait a moment and try again.\n")
                    raise SystemExit(1)
                except ProviderError as e:
                    import click
                    click.echo(f"\n❌ API error: {e}")
                    click.echo("🔑 Check your API key and provider settings.")
                    click.echo("👉 Run: autopr configure\n")
                    raise SystemExit(1)
            return _safe_call
        return attr

llm = LazyProviderProxy()
