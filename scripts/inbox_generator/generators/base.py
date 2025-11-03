"""
Base Generator Interface

Defines the contract for all content generators.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..core.config_loader import ContentElement


class BaseGenerator(ABC):
    """
    Abstract base class for content generators.

    All generators must implement the generate() method.
    """

    @abstractmethod
    def generate(
        self,
        element: ContentElement,
        context: Dict[str, Any],
        config_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate content for a single element.

        Args:
            element: The content element to generate
            context: User-provided context data
            config_metadata: Optional metadata from the content config

        Returns:
            Generated content as string

        Raises:
            ValueError: If required context is missing
            RuntimeError: If generation fails
        """
        pass

    def validate_context(
        self,
        element: ContentElement,
        context: Dict[str, Any],
        required_fields: list[str]
    ) -> None:
        """
        Validate that required context fields are present.

        Args:
            element: The content element being generated
            context: User-provided context data
            required_fields: List of required field names

        Raises:
            ValueError: If required fields are missing
        """
        missing = [field for field in required_fields if field not in context]
        if missing:
            raise ValueError(
                f"Missing required context for element '{element.id}': {missing}"
            )
