# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ITemplateRenderer Domain Port.

Defines the interface that all template-rendering adapters must satisfy.
The domain layer depends on this Protocol; infrastructure adapters implement it.
This keeps the domain free from any Jinja2 import or file-system awareness.

Location: src/docs/domain/ports/template_renderer.py
Reference: doc-module-spec.md Section: Output Rendering
           Threat Model M-2: SandboxedEnvironment required
"""

from typing import Any, Protocol


class ITemplateRenderer(Protocol):
    """Port for rendering Jinja2 template sections into markdown strings.

    Implementations:
        - Jinja2Renderer: uses ``jinja2.sandbox.SandboxedEnvironment``
          (src/docs/infrastructure/adapters/jinja2_renderer.py)

    Security note (M-2): Implementations MUST use ``SandboxedEnvironment``
    with ``StrictUndefined`` to prevent template injection (OWASP A03:2021).
    """

    def render_section(self, template_name: str, context: dict[str, Any]) -> str:
        """Render a named template with the provided context variables.

        Args:
            template_name: Filename of the template relative to the templates
                directory (e.g., ``"skills-table.md.jinja2"``).
            context: Mapping of variable names to values available inside the
                template.  All values should be sanitized before this call
                (M-1 caller responsibility).

        Returns:
            The fully rendered markdown string.

        Raises:
            FileNotFoundError: If ``template_name`` is not found in the
                configured template directory.
            ValueError: If the template references an undefined variable
                (``StrictUndefined`` mode enforced by implementations).
            RuntimeError: If the template has a syntax error or sandboxed
                execution is violated (E-1 mitigation).
        """
        ...

    def inject_between_markers(
        self,
        readme_content: str,
        section_name: str,
        generated_content: str,
    ) -> str:
        """Replace content between BEGIN/END marker comments in README text.

        Finds the ``<!-- BEGIN:GENERATED:{section_name} -->`` and
        ``<!-- END:GENERATED:{section_name} -->`` pair and replaces
        everything between them with ``generated_content``.

        Args:
            readme_content: The full current README.md text.
            section_name: Marker identifier, e.g., ``"SKILLS_TABLE"`` or
                ``"FEATURES"``.
            generated_content: The newly rendered markdown to inject.

        Returns:
            Updated README text with the section replaced.

        Raises:
            ValueError: If the expected marker pair is not found in
                ``readme_content`` (spec exit code 2).
        """
        ...
