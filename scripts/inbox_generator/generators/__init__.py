"""
Content Generators

Exports all generator classes and factory function.
"""

from .base import BaseGenerator
from .literal import LiteralGenerator
from .user_input import UserInputGenerator
from .template import TemplateGenerator
from .ai_augmented import AIAugmentedGenerator


def get_generator(generation_pattern: str, **kwargs) -> BaseGenerator:
    """
    Factory function to get the appropriate generator for a pattern.

    Args:
        generation_pattern: The generation pattern name
            - "literal": Returns LiteralGenerator
            - "user_input": Returns UserInputGenerator
            - "template_fill": Returns TemplateGenerator
            - "ai_augmented": Returns AIAugmentedGenerator
        **kwargs: Additional arguments to pass to generator constructor
                 (e.g., model, api_key for AIAugmentedGenerator)

    Returns:
        Generator instance

    Raises:
        ValueError: If pattern is unknown
    """
    generators = {
        'literal': LiteralGenerator,
        'user_input': UserInputGenerator,
        'template_fill': TemplateGenerator,
        'ai_augmented': AIAugmentedGenerator,
    }

    if generation_pattern not in generators:
        raise ValueError(
            f"Unknown generation pattern: {generation_pattern}. "
            f"Valid patterns: {list(generators.keys())}"
        )

    generator_class = generators[generation_pattern]

    # Only AIAugmentedGenerator accepts kwargs
    if generation_pattern == 'ai_augmented':
        return generator_class(**kwargs)
    else:
        return generator_class()


__all__ = [
    'BaseGenerator',
    'LiteralGenerator',
    'UserInputGenerator',
    'TemplateGenerator',
    'AIAugmentedGenerator',
    'get_generator',
]
