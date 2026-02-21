# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
JerryDocument - Unified facade for Jerry markdown AST operations.

Provides a single entry point for all markdown parsing, querying, transforming,
and rendering operations used throughout the Jerry Framework. Built on
markdown-it-py for parsing and mdformat for rendering.

The Jerry frontmatter blockquote pattern (validated in R-01 PoC):
    > **Key:** value

is accessible via query('blockquote') and text extraction from the parsed tree.

References:
    - ST-001: JerryDocument Facade
    - R-01: markdown-it-py + mdformat PoC validation
    - H-07: Domain layer MUST NOT import application/infrastructure/interface layers

Exports:
    JerryDocument: Unified facade for markdown AST operations
"""

from __future__ import annotations

import copy
from collections.abc import Callable

import mdformat
from markdown_it import MarkdownIt
from markdown_it.token import Token
from markdown_it.tree import SyntaxTreeNode


class JerryDocument:
    """
    Unified facade for Jerry markdown AST operations.

    Wraps markdown-it-py and mdformat to provide a single, consistent API for
    parsing, querying, transforming, and rendering markdown documents used in
    the Jerry Framework (worktracker items, plans, knowledge files, etc.).

    Instances are immutable after construction. All mutation operations (such as
    transform) return a new JerryDocument rather than modifying in place.

    Attributes:
        source: The original markdown source text.
        tree: The parsed SyntaxTreeNode AST root.
        tokens: The flat token list produced by markdown-it-py.

    Examples:
        >>> doc = JerryDocument.parse("# Hello\\n\\nSome text\\n")
        >>> doc.query("heading")
        [<SyntaxTreeNode heading>]
        >>> doc.render()
        '# Hello\\n\\nSome text\\n'
    """

    _md: MarkdownIt = MarkdownIt("commonmark")

    def __init__(
        self,
        source: str,
        tokens: list[Token],
        tree: SyntaxTreeNode,
    ) -> None:
        """
        Initialize a JerryDocument with pre-parsed components.

        Prefer JerryDocument.parse() for constructing instances from raw source.

        Args:
            source: The original markdown source text.
            tokens: The flat token list from markdown-it-py.
            tree: The SyntaxTreeNode AST root built from tokens.
        """
        self._source = source
        self._tokens = tokens
        self._tree = tree

    @classmethod
    def parse(cls, source: str) -> JerryDocument:
        """
        Parse markdown source text into a JerryDocument.

        Uses markdown-it-py in commonmark mode to tokenize and build an AST.
        The original source is preserved unchanged; rendering via render() may
        apply mdformat normalization.

        Args:
            source: Markdown source text to parse. May be empty.

        Returns:
            A new JerryDocument containing the parsed AST and original source.

        Examples:
            >>> doc = JerryDocument.parse("# Hello\\n")
            >>> doc.tree.type
            'root'
            >>> doc.source
            '# Hello\\n'
        """
        tokens = cls._md.parse(source)
        tree = SyntaxTreeNode(tokens)
        return cls(source, tokens, tree)

    def render(self) -> str:
        """
        Render the document back to normalized markdown via mdformat.

        Applies mdformat normalization to the stored source text. The first
        call may change whitespace or formatting; subsequent parse-render cycles
        on the resulting text are idempotent.

        Returns:
            Normalized markdown string. For empty source, returns an empty string.

        Examples:
            >>> doc = JerryDocument.parse("# Hello\\n\\nSome text\\n")
            >>> doc.render()
            '# Hello\\n\\nSome text\\n'
        """
        if not self._source:
            return ""
        return mdformat.text(self._source)

    def query(self, node_type: str) -> list[SyntaxTreeNode]:
        """
        Query all nodes of a given type in the document AST.

        Walks the full AST tree and collects every non-root node whose type
        matches the requested node_type string. Node types correspond to
        markdown-it-py SyntaxTreeNode type names (e.g., 'heading', 'paragraph',
        'blockquote', 'bullet_list', 'inline').

        Args:
            node_type: The node type string to match (case-sensitive).
                Common values: 'heading', 'paragraph', 'blockquote',
                'bullet_list', 'ordered_list', 'inline', 'code_block', 'fence'.

        Returns:
            List of matching SyntaxTreeNode instances, in document order.
            Returns an empty list if no nodes of that type are found or if
            the document is empty.

        Examples:
            >>> doc = JerryDocument.parse("# H1\\n\\n## H2\\n")
            >>> headings = doc.query("heading")
            >>> len(headings)
            2
        """
        results: list[SyntaxTreeNode] = []
        for node in self._tree.walk():
            if node.is_root:
                continue
            if node.type == node_type:
                results.append(node)
        return results

    def transform(
        self,
        visitor: Callable[[SyntaxTreeNode], SyntaxTreeNode | None],
    ) -> JerryDocument:
        """
        Apply a visitor function to produce a new transformed JerryDocument.

        Creates a deep copy of the token list and AST tree, then walks the copy
        applying the visitor to each non-root node. The visitor may mutate the
        node's token content in place (or return None/the node unchanged).
        The resulting modified source is reconstructed from the original source
        lines with changed inline content substituted, then re-parsed.

        This method is immutable: the original JerryDocument is never modified.

        Args:
            visitor: A callable that receives a SyntaxTreeNode and returns the
                node (possibly mutated) or None (treated as no-op). The visitor
                SHOULD only modify token.content on 'inline' nodes for
                predictable source reconstruction. Structural modifications
                (adding/removing nodes) are not supported.

        Returns:
            A new JerryDocument built from the transformed source text.

        Examples:
            >>> doc = JerryDocument.parse("# Hello\\n")
            >>> def uppercaser(node):
            ...     if node.type == 'inline':
            ...         node.token.content = node.token.content.upper()
            ...     return node
            >>> new_doc = doc.transform(uppercaser)
            >>> new_doc.render()
            '# HELLO\\n'
        """
        # Deep copy tokens so original is never mutated
        copied_tokens = copy.deepcopy(self._tokens)
        copied_tree = SyntaxTreeNode(copied_tokens)

        # Snapshot original inline content keyed by (start_line)
        # so we can detect what changed after visiting
        orig_inline_map: dict[int, str] = {}
        for token in self._tokens:
            if token.type == "inline" and token.map is not None:
                orig_inline_map[token.map[0]] = token.content

        # Apply visitor to all non-root nodes
        for node in copied_tree.walk():
            if node.is_root:
                continue
            visitor(node)

        # Build map of changed inline content: start_line -> new_content
        modified_tokens = copied_tree.to_tokens()
        new_inline_map: dict[int, str] = {}
        for token in modified_tokens:
            if token.type == "inline" and token.map is not None:
                new_inline_map[token.map[0]] = token.content

        # Reconstruct modified source by substituting changed inline content
        source_lines = self._source.split("\n")
        result_lines = list(source_lines)

        for line_idx, new_content in new_inline_map.items():
            orig_content = orig_inline_map.get(line_idx)
            if (
                orig_content is not None
                and orig_content != new_content
                and line_idx < len(result_lines)
            ):
                original_line = source_lines[line_idx]
                if orig_content in original_line:
                    result_lines[line_idx] = original_line.replace(orig_content, new_content, 1)

        modified_source = "\n".join(result_lines)
        return JerryDocument.parse(modified_source)

    @property
    def source(self) -> str:
        """
        The original source text provided to parse().

        Returns:
            The unmodified markdown source string.
        """
        return self._source

    @property
    def tree(self) -> SyntaxTreeNode:
        """
        The AST tree root node.

        Returns:
            The SyntaxTreeNode root of the parsed document. Its type is 'root'.
        """
        return self._tree

    @property
    def tokens(self) -> list[Token]:
        """
        The flat token list produced by markdown-it-py.

        Returns a shallow copy to prevent external mutation of the internal
        token list. Individual Token objects are shared (not deep-copied)
        for performance.

        Returns:
            List of Token objects in document order. Inline tokens are in the
            flat list; their children are inline-level tokens accessible via
            Token.children.
        """
        return list(self._tokens)
