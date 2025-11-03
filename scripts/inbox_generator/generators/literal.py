"""
Literal Generator - Returns hardcoded values

Used for fields that always have the same value (e.g., type: "coordination")
"""

from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..core.config_loader import ContentElement


class LiteralGenerator(BaseGenerator):
    """
    Generates content from hardcoded literal values.

    Example:
        element.example_output = "coordination"
        -> Returns: "coordination"
    """

    def generate(
        self,
        element: ContentElement,
        context: Dict[str, Any],
        config_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Return the literal value from example_output.

        Args:
            element: Content element with example_output field
            context: User context (unused for literals)
            config_metadata: Config metadata (unused)

        Returns:
            The literal value from element.example_output

        Raises:
            ValueError: If example_output is not set
        """
        if not element.example_output:
            raise ValueError(
                f"Literal generator requires example_output for element: {element.id}"
            )

        return element.example_output
