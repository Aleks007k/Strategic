"""
Strategic AI Core Backend
LLM providers package
"""

from engines.providers.mock_provider import MockProvider
from engines.providers.anthropic_provider import AnthropicProvider
from engines.providers.openai_provider import OpenAIProvider
from engines.providers.ollama_provider import OllamaProvider

PROVIDERS = {
    "mock": MockProvider,
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,
    "ollama": OllamaProvider,
}
