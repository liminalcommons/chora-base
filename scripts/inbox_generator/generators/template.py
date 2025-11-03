"""
Template Generator - Uses Jinja2 templates

Used for fields that follow a pattern but use dynamic values (e.g., request_id: "COORD-{year}-{number}")
"""

from typing import Any, Dict, Optional
from jinja2 import Template, TemplateSyntaxError, UndefinedError
from .base import BaseGenerator
from ..core.config_loader import ContentElement


class TemplateGenerator(BaseGenerator):
    """
    Generates content using Jinja2 templates.

    Example:
        element.template = "COORD-{{year}}-{{number}}"
        context = {"year": "2025", "number": "005"}
        -> Returns: "COORD-2025-005"
    """

    def generate(
        self,
        element: ContentElement,
        context: Dict[str, Any],
        config_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Render Jinja2 template with context data.

        Args:
            element: Content element with template field
            context: User-provided context data
            config_metadata: Config metadata (available in template as 'metadata')

        Returns:
            Rendered template string

        Raises:
            ValueError: If template is missing or invalid
            RuntimeError: If template rendering fails
        """
        if not element.template:
            raise ValueError(
                f"Template generator requires template for element: {element.id}"
            )

        try:
            # Create Jinja2 template
            template = Template(element.template)

            # Prepare template context
            template_context = context.copy()
            if config_metadata:
                template_context['metadata'] = config_metadata

            # Render template
            result = template.render(**template_context)
            return result

        except TemplateSyntaxError as e:
            raise ValueError(
                f"Invalid template syntax in element '{element.id}': {e}"
            )
        except UndefinedError as e:
            raise RuntimeError(
                f"Template rendering failed for element '{element.id}': {e}\n"
                f"Available context keys: {list(context.keys())}"
            )
        except Exception as e:
            raise RuntimeError(
                f"Template generation failed for element '{element.id}': {e}"
            )

    def validate_template(self, template_str: str) -> bool:
        """
        Validate that a template string is syntactically correct.

        Args:
            template_str: The Jinja2 template string

        Returns:
            True if valid, False otherwise
        """
        try:
            Template(template_str)
            return True
        except TemplateSyntaxError:
            return False
