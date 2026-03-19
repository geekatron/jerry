# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Jinja2Renderer Infrastructure Adapter.

Implements ITemplateRenderer using jinja2.sandbox.SandboxedEnvironment
with StrictUndefined for safe template rendering.

Location: src/docs/infrastructure/adapters/jinja2_renderer.py
Reference: doc-module-spec.md Section: Output Rendering
           M-2: SandboxedEnvironment + StrictUndefined
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.sandbox import SandboxedEnvironment

from src.docs.domain.ports.template_renderer import ITemplateRenderer


class Jinja2Renderer(ITemplateRenderer):
    """Template renderer using Jinja2 SandboxedEnvironment.

    Security controls (M-2):
        - ``SandboxedEnvironment`` prevents template code from accessing
          unsafe attributes or calling dangerous methods.
        - ``StrictUndefined`` raises an error on any undefined variable
          reference, preventing silent data leakage.
        - ``autoescape=False`` is safe because output is markdown, not HTML.

    Attributes:
        _env: The configured Jinja2 sandboxed environment.
    """

    def __init__(self, template_dir: str) -> None:
        """Initialize with a template directory.

        Args:
            template_dir: Path to the directory containing Jinja2 templates
                (e.g., ``.context/templates/docs/``).

        Raises:
            FileNotFoundError: If ``template_dir`` does not exist on the
                filesystem.
        """
        template_path = Path(template_dir)
        if not template_path.is_dir():
            raise FileNotFoundError(
                f"Template directory not found: '{template_dir}'. "
                f"Ensure you are running from the repository root."
            )
        self._env = SandboxedEnvironment(
            loader=FileSystemLoader(template_dir),
            undefined=StrictUndefined,
            autoescape=False,
        )

    def render_section(self, template_name: str, context: dict[str, Any]) -> str:
        """Render a named template with the provided context variables.

        Args:
            template_name: Filename of the template relative to the templates
                directory (e.g., ``"skills-table.md.jinja2"``).
            context: Mapping of variable names to values available inside the
                template.

        Returns:
            The fully rendered markdown string.

        Raises:
            FileNotFoundError: If ``template_name`` is not found.
            ValueError: If the template references an undefined variable.
            RuntimeError: If the template has a syntax error or sandboxed
                execution is violated.
        """
        try:
            template = self._env.get_template(template_name)
        except Exception as e:
            if "not found" in str(e).lower() or "TemplateNotFound" in type(e).__name__:
                raise FileNotFoundError(
                    f"Template '{template_name}' not found in template directory"
                ) from e
            raise RuntimeError(f"Template error: {e}") from e

        try:
            return template.render(**context)
        except Exception as e:
            if "UndefinedError" in type(e).__name__:
                raise ValueError(f"Undefined variable in template: {e}") from e
            raise RuntimeError(f"Template rendering error: {e}") from e

    def inject_between_markers(
        self,
        readme_content: str,
        section_name: str,
        generated_content: str,
    ) -> str:
        """Replace content between BEGIN/END marker comments in README text.

        Args:
            readme_content: The full current README.md text.
            section_name: Marker identifier (e.g., ``"SKILLS_TABLE"``).
            generated_content: The newly rendered markdown to inject.

        Returns:
            Updated README text with the section replaced.

        Raises:
            ValueError: If the expected marker pair is not found.
        """
        begin_marker = f"<!-- BEGIN:GENERATED:{section_name} -->"
        end_marker = f"<!-- END:GENERATED:{section_name} -->"

        if begin_marker not in readme_content or end_marker not in readme_content:
            raise ValueError(
                f"Marker pair not found in README content: {begin_marker} / {end_marker}"
            )

        begin_idx = readme_content.index(begin_marker) + len(begin_marker)
        end_idx = readme_content.index(end_marker)

        if begin_idx > end_idx:
            raise ValueError(
                f"Inverted marker order for section {section_name}: "
                f"BEGIN at {begin_idx}, END at {end_idx}"
            )

        return (
            readme_content[:begin_idx] + "\n" + generated_content + "\n" + readme_content[end_idx:]
        )
