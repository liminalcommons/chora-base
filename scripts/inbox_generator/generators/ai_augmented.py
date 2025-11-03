"""
AI Augmented Generator - Uses AI to generate/transform content

Used for complex fields that need AI assistance (e.g., deliverables, acceptance criteria)
"""

import os
import json
from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..core.config_loader import ContentElement


class AIAugmentedGenerator(BaseGenerator):
    """
    Generates content using AI (Claude or OpenAI).

    This generator uses a prompt template to instruct the AI on how to generate
    or transform content based on user context.

    Example:
        element.prompt_template = "Generate 5-8 SMART acceptance criteria for: {{description}}"
        context = {"description": "Add dark mode support"}
        -> Returns: AI-generated acceptance criteria list
    """

    def __init__(self, model: str = "claude-sonnet-4-5-20250929", api_key: Optional[str] = None):
        """
        Initialize AI generator.

        Args:
            model: Model to use (claude-sonnet-4-5-20250929 or gpt-4, etc.)
            api_key: API key (defaults to ANTHROPIC_API_KEY or OPENAI_API_KEY env var)
        """
        self.model = model
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY') or os.getenv('OPENAI_API_KEY')

        if not self.api_key:
            raise ValueError(
                "AI generator requires ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable"
            )

        # Detect provider from model name
        if 'claude' in model.lower():
            self.provider = 'anthropic'
        elif 'gpt' in model.lower():
            self.provider = 'openai'
        else:
            raise ValueError(f"Unknown model provider for: {model}")

    def generate(
        self,
        element: ContentElement,
        context: Dict[str, Any],
        config_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate content using AI.

        Args:
            element: Content element with prompt_template field
            context: User-provided context data
            config_metadata: Config metadata (available in prompt as 'metadata')

        Returns:
            AI-generated content

        Raises:
            ValueError: If prompt_template is missing
            RuntimeError: If AI generation fails
        """
        if not element.prompt_template:
            raise ValueError(
                f"AI generator requires prompt_template for element: {element.id}"
            )

        # Render prompt template with context
        from jinja2 import Template
        prompt_template = Template(element.prompt_template)
        template_context = context.copy()
        if config_metadata:
            template_context['metadata'] = config_metadata

        prompt = prompt_template.render(**template_context)

        # Generate using appropriate provider
        if self.provider == 'anthropic':
            return self._generate_anthropic(prompt, element)
        elif self.provider == 'openai':
            return self._generate_openai(prompt, element)
        else:
            raise RuntimeError(f"Unknown provider: {self.provider}")

    def _generate_anthropic(self, prompt: str, element: ContentElement) -> str:
        """
        Generate content using Anthropic Claude API.

        Args:
            prompt: The rendered prompt
            element: Content element being generated

        Returns:
            Generated content

        Raises:
            RuntimeError: If API call fails
        """
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            message = client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.3,  # Lower temperature for more consistent output
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract text from response
            result = message.content[0].text

            # If element expects JSON and result contains JSON, extract it
            if element.example_output and (
                element.example_output.startswith('[') or
                element.example_output.startswith('{')
            ):
                result = self._extract_json(result)

            return result

        except Exception as e:
            raise RuntimeError(
                f"Anthropic AI generation failed for element '{element.id}': {e}"
            )

    def _generate_openai(self, prompt: str, element: ContentElement) -> str:
        """
        Generate content using OpenAI API.

        Args:
            prompt: The rendered prompt
            element: Content element being generated

        Returns:
            Generated content

        Raises:
            RuntimeError: If API call fails
        """
        try:
            import openai

            client = openai.OpenAI(api_key=self.api_key)

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=4096
            )

            result = response.choices[0].message.content

            # If element expects JSON and result contains JSON, extract it
            if element.example_output and (
                element.example_output.startswith('[') or
                element.example_output.startswith('{')
            ):
                result = self._extract_json(result)

            return result

        except Exception as e:
            raise RuntimeError(
                f"OpenAI generation failed for element '{element.id}': {e}"
            )

    def _extract_json(self, text: str) -> str:
        """
        Extract JSON from AI response that may contain markdown formatting.

        Args:
            text: AI response text

        Returns:
            Clean JSON string or original text if no JSON found
        """
        # Remove markdown code blocks
        if '```json' in text:
            # Extract content between ```json and ```
            start = text.find('```json') + 7
            end = text.find('```', start)
            if end != -1:
                text = text[start:end].strip()
        elif '```' in text:
            # Extract content between ``` and ```
            start = text.find('```') + 3
            end = text.find('```', start)
            if end != -1:
                text = text[start:end].strip()

        # Validate it's actually JSON
        try:
            json.loads(text)
            return text
        except json.JSONDecodeError:
            # Return original if not valid JSON
            return text
