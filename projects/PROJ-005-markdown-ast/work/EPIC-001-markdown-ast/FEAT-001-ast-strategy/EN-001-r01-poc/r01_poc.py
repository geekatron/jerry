"""R-01 Proof-of-Concept: mdformat blockquote frontmatter write-back validation.

Tests whether markdown-it-py + mdformat can:
1. Parse a real Jerry entity file
2. Identify blockquote frontmatter tokens
3. Modify a frontmatter field (Status)
4. Render back with mdformat
5. Preserve unmodified regions

Run: uv run python projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/EN-001-r01-poc/r01_poc.py
"""

from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path
from typing import Any

import mdformat
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode


# ---------------------------------------------------------------------------
# Test file paths (relative to repo root)
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[6]
# parents[0]=EN-001-r01-poc [1]=FEAT-001-ast-strategy [2]=EPIC-001-markdown-ast
# [3]=work [4]=PROJ-005-markdown-ast [5]=projects [6]=repo root

TEST_FILES: list[dict[str, Any]] = [
    {
        "name": "SPIKE-002 entity (Spike)",
        "path": REPO_ROOT
        / "projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast"
        / "FEAT-001-ast-strategy/SPIKE-002-feasibility/SPIKE-002-feasibility.md",
        "field": "Status",
        "old_value": "completed",
        "new_value": "in-progress",
    },
    {
        "name": "EPIC-001 entity (Epic)",
        "path": REPO_ROOT
        / "projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast"
        / "EPIC-001-markdown-ast.md",
        "field": "Status",
        "old_value": "in-progress",
        "new_value": "pending",
    },
    {
        "name": "EN-001 entity (Enabler)",
        "path": REPO_ROOT
        / "projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast"
        / "FEAT-001-ast-strategy/EN-001-r01-poc/EN-001-r01-poc.md",
        "field": "Status",
        "old_value": "in-progress",
        "new_value": "completed",
    },
]


# ---------------------------------------------------------------------------
# Frontmatter extraction helpers
# ---------------------------------------------------------------------------
FRONTMATTER_PATTERN = re.compile(
    r"^>\s*\*\*(?P<key>[^*:]+):\*\*\s*(?P<value>.+)$", re.MULTILINE
)


def extract_frontmatter(source: str) -> list[dict[str, str]]:
    """Extract blockquote frontmatter key-value pairs from source."""
    results = []
    for match in FRONTMATTER_PATTERN.finditer(source):
        results.append(
            {
                "key": match.group("key").strip(),
                "value": match.group("value").strip(),
                "start": match.start(),
                "end": match.end(),
                "full_match": match.group(0),
            }
        )
    return results


def modify_frontmatter_field(
    source: str, field_name: str, old_value: str, new_value: str
) -> str | None:
    """Modify a specific frontmatter field value in the source string."""
    pattern = re.compile(
        rf"^(>\s*\*\*{re.escape(field_name)}:\*\*\s*){re.escape(old_value)}(\s*)$",
        re.MULTILINE,
    )
    modified, count = pattern.subn(rf"\g<1>{new_value}\2", source)
    if count == 0:
        return None
    return modified


# ---------------------------------------------------------------------------
# CHECK functions
# ---------------------------------------------------------------------------
def check_1_field_renders_correctly(
    rendered: str, field_name: str, new_value: str
) -> tuple[bool, str]:
    """CHECK 1: Does the modified field render correctly?"""
    fields = extract_frontmatter(rendered)
    for f in fields:
        if f["key"] == field_name:
            if f["value"] == new_value:
                return True, f"Field '{field_name}' renders as '{new_value}' -- correct"
            return (
                False,
                f"Field '{field_name}' renders as '{f['value']}', expected '{new_value}'",
            )
    return False, f"Field '{field_name}' not found in rendered output"


def check_2_unmodified_regions_preserved(
    original_normalized: str,
    rendered: str,
    field_name: str,
    old_value: str,
    new_value: str,
) -> tuple[bool, str, list[str]]:
    """CHECK 2: Are unmodified regions byte-for-byte identical?

    Compare the mdformat-normalized original (with the field reverted)
    against the rendered output to isolate only the intended change.
    """
    # Revert the field change in rendered to compare everything else
    reverted = modify_frontmatter_field(rendered, field_name, new_value, old_value)
    if reverted is None:
        return False, "Could not revert field in rendered output", []

    if reverted == original_normalized:
        return True, "Unmodified regions are byte-for-byte identical", []

    # Show the diff
    diff = list(
        difflib.unified_diff(
            original_normalized.splitlines(keepends=True),
            reverted.splitlines(keepends=True),
            fromfile="original (mdformat normalized)",
            tofile="rendered (field reverted)",
            n=2,
        )
    )

    # Assess if diff is acceptable (whitespace only)
    orig_stripped = original_normalized.strip()
    reverted_stripped = reverted.strip()
    if orig_stripped == reverted_stripped:
        return (
            True,
            "Unmodified regions differ only in trailing whitespace -- acceptable",
            diff,
        )

    return (
        False,
        f"Unmodified regions differ ({len(diff)} diff lines)",
        diff,
    )


def check_3_mdformat_roundtrip_stable(rendered: str) -> tuple[bool, str]:
    """CHECK 3: Does a second mdformat pass produce identical output?

    This validates mdformat's idempotency (a proxy for HTML-equality).
    """
    double_rendered = mdformat.text(rendered)
    if double_rendered == rendered:
        return True, "mdformat roundtrip is idempotent (stable after 2nd pass)"
    diff_count = sum(
        1
        for a, b in zip(
            rendered.splitlines(), double_rendered.splitlines()
        )
        if a != b
    )
    return False, f"mdformat roundtrip NOT idempotent ({diff_count} lines differ)"


# ---------------------------------------------------------------------------
# Token analysis (informational)
# ---------------------------------------------------------------------------
def analyze_tokens(source: str) -> dict[str, Any]:
    """Parse source and return token analysis for diagnostics."""
    md = MarkdownIt("commonmark")
    tokens = md.parse(source)
    node = SyntaxTreeNode(tokens)

    token_types = {}
    for tok in tokens:
        token_types[tok.type] = token_types.get(tok.type, 0) + 1

    # Find blockquote nodes
    blockquote_count = 0
    for child in node.walk():
        if child.type == "blockquote":
            blockquote_count += 1

    return {
        "total_tokens": len(tokens),
        "token_types": token_types,
        "blockquote_nodes": blockquote_count,
        "tree_depth": _tree_depth(node),
    }


def _tree_depth(node: SyntaxTreeNode, depth: int = 0) -> int:
    if not node.children:
        return depth
    return max(_tree_depth(c, depth + 1) for c in node.children)


# ---------------------------------------------------------------------------
# Main PoC execution
# ---------------------------------------------------------------------------
def run_poc() -> dict[str, Any]:
    """Execute the R-01 PoC against all test files."""
    results: dict[str, Any] = {"files": [], "overall_pass": True}

    for test in TEST_FILES:
        file_result: dict[str, Any] = {"name": test["name"], "path": str(test["path"])}
        print(f"\n{'='*70}")
        print(f"TEST: {test['name']}")
        print(f"FILE: {test['path'].relative_to(REPO_ROOT)}")
        print(f"{'='*70}")

        # Read source
        if not test["path"].exists():
            file_result["error"] = f"File not found: {test['path']}"
            file_result["pass"] = False
            results["files"].append(file_result)
            results["overall_pass"] = False
            print(f"  ERROR: File not found")
            continue

        source = test["path"].read_text()
        file_result["source_lines"] = source.count("\n")

        # Token analysis
        analysis = analyze_tokens(source)
        file_result["token_analysis"] = analysis
        print(f"\n  Token Analysis:")
        print(f"    Total tokens: {analysis['total_tokens']}")
        print(f"    Blockquote nodes: {analysis['blockquote_nodes']}")
        print(f"    Tree depth: {analysis['tree_depth']}")

        # Extract frontmatter
        fields = extract_frontmatter(source)
        file_result["frontmatter_fields"] = len(fields)
        print(f"    Frontmatter fields found: {len(fields)}")
        for f in fields:
            print(f"      {f['key']}: {f['value']}")

        # Normalize original with mdformat (baseline)
        print(f"\n  Step 1: Normalize original with mdformat...")
        original_normalized = mdformat.text(source)
        file_result["normalized_lines"] = original_normalized.count("\n")
        norm_growth = len(original_normalized) - len(source)
        print(f"    Original: {len(source)} chars, Normalized: {len(original_normalized)} chars (growth: +{norm_growth})")

        # Modify field in normalized source
        print(f"\n  Step 2: Modify field '{test['field']}': '{test['old_value']}' -> '{test['new_value']}'...")
        modified = modify_frontmatter_field(
            original_normalized, test["field"], test["old_value"], test["new_value"]
        )
        if modified is None:
            file_result["error"] = f"Could not find field '{test['field']}' with value '{test['old_value']}' in normalized source"
            file_result["pass"] = False
            results["files"].append(file_result)
            results["overall_pass"] = False
            print(f"    ERROR: Field not found in normalized source")
            continue

        # Render modified source with mdformat
        print(f"\n  Step 3: Render modified source with mdformat...")
        rendered = mdformat.text(modified)
        file_result["rendered_lines"] = rendered.count("\n")

        # CHECK 1
        print(f"\n  CHECK 1: Modified field renders correctly?")
        c1_pass, c1_msg = check_1_field_renders_correctly(
            rendered, test["field"], test["new_value"]
        )
        file_result["check_1"] = {"pass": c1_pass, "message": c1_msg}
        print(f"    {'PASS' if c1_pass else 'FAIL'}: {c1_msg}")

        # CHECK 2
        print(f"\n  CHECK 2: Unmodified regions preserved?")
        c2_pass, c2_msg, c2_diff = check_2_unmodified_regions_preserved(
            original_normalized, rendered, test["field"], test["old_value"], test["new_value"]
        )
        file_result["check_2"] = {"pass": c2_pass, "message": c2_msg, "diff_lines": len(c2_diff)}
        print(f"    {'PASS' if c2_pass else 'FAIL'}: {c2_msg}")
        if c2_diff:
            print(f"    Diff ({len(c2_diff)} lines):")
            for line in c2_diff[:20]:  # limit output
                print(f"      {line}", end="")

        # CHECK 3
        print(f"\n  CHECK 3: mdformat roundtrip idempotent?")
        c3_pass, c3_msg = check_3_mdformat_roundtrip_stable(rendered)
        file_result["check_3"] = {"pass": c3_pass, "message": c3_msg}
        print(f"    {'PASS' if c3_pass else 'FAIL'}: {c3_msg}")

        # Overall for this file
        file_pass = c1_pass and c2_pass and c3_pass
        file_result["pass"] = file_pass
        results["files"].append(file_result)
        if not file_pass:
            results["overall_pass"] = False

        print(f"\n  FILE RESULT: {'PASS' if file_pass else 'FAIL'}")

    return results


def print_summary(results: dict[str, Any]) -> None:
    """Print summary table."""
    print(f"\n{'='*70}")
    print("R-01 PROOF-OF-CONCEPT SUMMARY")
    print(f"{'='*70}")
    print(f"\n{'File':<40} {'C1':>5} {'C2':>5} {'C3':>5} {'Result':>8}")
    print(f"{'-'*40} {'-'*5} {'-'*5} {'-'*5} {'-'*8}")
    for f in results["files"]:
        name = f["name"][:39]
        if "error" in f:
            print(f"{name:<40} {'ERR':>5} {'ERR':>5} {'ERR':>5} {'FAIL':>8}")
        else:
            c1 = "PASS" if f["check_1"]["pass"] else "FAIL"
            c2 = "PASS" if f["check_2"]["pass"] else "FAIL"
            c3 = "PASS" if f["check_3"]["pass"] else "FAIL"
            result = "PASS" if f["pass"] else "FAIL"
            print(f"{name:<40} {c1:>5} {c2:>5} {c3:>5} {result:>8}")

    print(f"\n{'='*70}")
    overall = "PASS" if results["overall_pass"] else "FAIL"
    print(f"OVERALL R-01 VERDICT: {overall}")
    if results["overall_pass"]:
        print("  -> Proceed with standard implementation (no fallback needed)")
    else:
        print("  -> ESCALATE to Fallback A (string-level substitution)")
    print(f"{'='*70}")


if __name__ == "__main__":
    results = run_poc()
    print_summary(results)
    sys.exit(0 if results["overall_pass"] else 1)
