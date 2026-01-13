#!/usr/bin/env python3
"""
Playbook Validation Test Harness

Validates playbook examples for:
1. YAML syntax correctness
2. Placeholder text detection
3. File reference validation
4. Example structure validation

Part of WI-SAO-037: Validate all examples executable
"""

import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    check_name: str
    passed: bool
    details: str
    line_number: int | None = None
    severity: str = "ERROR"  # ERROR, WARNING, INFO


@dataclass
class PlaybookValidation:
    """Validation results for a single playbook."""
    playbook_path: str
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results if r.severity == "ERROR")

    @property
    def error_count(self) -> int:
        return sum(1 for r in self.results if not r.passed and r.severity == "ERROR")

    @property
    def warning_count(self) -> int:
        return sum(1 for r in self.results if not r.passed and r.severity == "WARNING")


def extract_code_blocks(content: str) -> list[tuple[str, str, int]]:
    """Extract code blocks with their language and line number."""
    blocks = []
    lines = content.split('\n')
    in_block = False
    block_lang = ""
    block_content = []
    block_start = 0

    for i, line in enumerate(lines, 1):
        if line.startswith('```') and not in_block:
            in_block = True
            block_lang = line[3:].strip()
            block_content = []
            block_start = i
        elif line.startswith('```') and in_block:
            in_block = False
            blocks.append((block_lang, '\n'.join(block_content), block_start))
        elif in_block:
            block_content.append(line)

    return blocks


def validate_yaml_syntax(content: str) -> tuple[bool, str]:
    """Validate YAML syntax without importing yaml library."""
    # Basic YAML structure validation
    errors = []
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        # Check for tabs (YAML should use spaces)
        if '\t' in line and not line.strip().startswith('#'):
            errors.append(f"Line {i}: Tab character found (use spaces)")

        # Check for inconsistent indentation
        if line and not line.startswith('#'):
            leading_spaces = len(line) - len(line.lstrip())
            if leading_spaces % 2 != 0 and line.strip():
                errors.append(f"Line {i}: Odd indentation ({leading_spaces} spaces)")

        # Check for unclosed quotes
        quote_count = line.count('"') - line.count('\\"')
        if quote_count % 2 != 0:
            errors.append(f"Line {i}: Unclosed double quote")

        single_quote_count = line.count("'") - line.count("\\'")
        if single_quote_count % 2 != 0:
            errors.append(f"Line {i}: Unclosed single quote")

    if errors:
        return False, "; ".join(errors[:3])  # Limit to first 3 errors
    return True, "Valid YAML structure"


def check_placeholders(content: str) -> list[tuple[int, str]]:
    """Check for placeholder text patterns."""
    placeholder_patterns = [
        r'\{TODO\}',
        r'\{TBD\}',
        r'\[TODO\]',
        r'\[TBD\]',
        r'FIXME',
        r'\{\.\.\.\}',
        r'<INSERT.*?>',
        r'<REPLACE.*?>',
    ]
    # Patterns to exclude (valid use of XXX in naming conventions)
    exclude_patterns = [
        r'work-XXX',  # work-XXX-topic.md is a valid naming convention
        r'XXX-\d+',   # XXX-001 style IDs
        r'XXX-e-',    # XXX-e-001 style evidence IDs
    ]

    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        # First check exclusions - if any match, skip this line
        should_skip = any(re.search(excl, line) for excl in exclude_patterns)
        if should_skip:
            continue

        for pattern in placeholder_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append((i, f"Placeholder pattern found: {pattern}"))

    return findings


def check_file_references(content: str, base_path: Path) -> list[tuple[int, str, bool]]:
    """Check that referenced files/directories exist."""
    # Pattern for markdown links and file paths
    path_patterns = [
        r'\[.*?\]\(([^)]+\.md)\)',  # Markdown links to .md files
        r'\[.*?\]\(([^)]+\.yaml)\)',  # Markdown links to .yaml files
        r'`([^`]+/[^`]+\.(md|yaml|py))`',  # Inline code paths
    ]

    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        for pattern in path_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                # Handle tuple from groups
                if isinstance(match, tuple):
                    ref_path = match[0]
                else:
                    ref_path = match

                # Skip URLs
                if ref_path.startswith('http'):
                    continue

                # Skip template patterns like {PROJECT}, {topic}
                if '{' in ref_path or '[' in ref_path:
                    continue

                # Resolve relative paths
                if ref_path.startswith('../'):
                    full_path = base_path.parent / ref_path
                elif ref_path.startswith('./'):
                    full_path = base_path.parent / ref_path[2:]
                else:
                    full_path = base_path.parent / ref_path

                exists = full_path.exists()
                findings.append((i, ref_path, exists))

    return findings


def check_quick_reference_prompts(content: str) -> list[ValidationResult]:
    """Validate Quick Reference Card prompts have proper structure."""
    results = []

    # Find Quick Reference Card section
    if "## Quick Reference Card" not in content and "Quick Reference" not in content:
        return results

    # Extract table rows
    table_pattern = r'\|\s*([^|]+)\s*\|\s*`([^`]+)`\s*\|'
    matches = re.findall(table_pattern, content)

    for task, prompt in matches:
        # Check prompt has placeholder pattern
        if '{' not in prompt and '[' not in prompt:
            # Prompts without placeholders might be too specific
            results.append(ValidationResult(
                check_name="prompt_flexibility",
                passed=True,
                details=f"Prompt '{prompt[:30]}...' is concrete",
                severity="INFO"
            ))

        # Check prompt is not empty
        if not prompt.strip():
            results.append(ValidationResult(
                check_name="prompt_empty",
                passed=False,
                details=f"Task '{task}' has empty prompt",
                severity="ERROR"
            ))

    return results


def validate_playbook(playbook_path: Path) -> PlaybookValidation:
    """Run all validations on a playbook."""
    validation = PlaybookValidation(playbook_path=str(playbook_path))

    try:
        content = playbook_path.read_text()
    except Exception as e:
        validation.results.append(ValidationResult(
            check_name="file_read",
            passed=False,
            details=f"Could not read file: {e}",
            severity="ERROR"
        ))
        return validation

    # Check 1: Version header present
    if "**Version:**" in content:
        version_match = re.search(r'\*\*Version:\*\*\s*(\d+\.\d+\.\d+)', content)
        if version_match:
            validation.results.append(ValidationResult(
                check_name="version_header",
                passed=True,
                details=f"Version {version_match.group(1)} found"
            ))
        else:
            validation.results.append(ValidationResult(
                check_name="version_header",
                passed=False,
                details="Version format invalid (expected X.Y.Z)",
                severity="WARNING"
            ))
    else:
        validation.results.append(ValidationResult(
            check_name="version_header",
            passed=False,
            details="No version header found",
            severity="WARNING"
        ))

    # Check 2: Triple-lens structure present
    for section in ["# L0:", "# L1:", "# L2:"]:
        if section in content:
            validation.results.append(ValidationResult(
                check_name=f"section_{section[2:4]}",
                passed=True,
                details=f"Section {section} found"
            ))
        else:
            validation.results.append(ValidationResult(
                check_name=f"section_{section[2:4]}",
                passed=False,
                details=f"Section {section} missing",
                severity="ERROR"
            ))

    # Check 3: YAML code blocks
    code_blocks = extract_code_blocks(content)
    yaml_blocks = [(lang, block, line) for lang, block, line in code_blocks if lang in ('yaml', 'yml')]

    for _lang, block, line_num in yaml_blocks:
        valid, msg = validate_yaml_syntax(block)
        validation.results.append(ValidationResult(
            check_name="yaml_syntax",
            passed=valid,
            details=msg,
            line_number=line_num,
            severity="ERROR" if not valid else "INFO"
        ))

    # Check 4: Placeholder text
    placeholders = check_placeholders(content)
    if placeholders:
        for line_num, desc in placeholders:
            validation.results.append(ValidationResult(
                check_name="placeholder_text",
                passed=False,
                details=desc,
                line_number=line_num,
                severity="ERROR"
            ))
    else:
        validation.results.append(ValidationResult(
            check_name="placeholder_text",
            passed=True,
            details="No placeholder text found"
        ))

    # Check 5: File references
    file_refs = check_file_references(content, playbook_path)
    missing_refs = [(line, path) for line, path, exists in file_refs if not exists]
    valid_refs = [(line, path) for line, path, exists in file_refs if exists]

    if missing_refs:
        for line_num, path in missing_refs[:5]:  # Limit to first 5
            validation.results.append(ValidationResult(
                check_name="file_reference",
                passed=False,
                details=f"Referenced file not found: {path}",
                line_number=line_num,
                severity="WARNING"
            ))

    if valid_refs:
        validation.results.append(ValidationResult(
            check_name="file_reference",
            passed=True,
            details=f"{len(valid_refs)} file references validated"
        ))

    # Check 6: Quick reference prompts
    prompt_results = check_quick_reference_prompts(content)
    validation.results.extend(prompt_results)

    # Check 7: Anti-pattern catalog (L2)
    if "## Anti-Pattern Catalog" in content or "Anti-Pattern" in content:
        ap_count = len(re.findall(r'### AP-\d+:', content))
        if ap_count >= 3:
            validation.results.append(ValidationResult(
                check_name="antipattern_coverage",
                passed=True,
                details=f"{ap_count} anti-patterns documented"
            ))
        else:
            validation.results.append(ValidationResult(
                check_name="antipattern_coverage",
                passed=False,
                details=f"Only {ap_count} anti-patterns (need ≥3)",
                severity="WARNING"
            ))

    # Check 8: ASCII diagrams present
    ascii_pattern = r'\+[-=]+\+'  # Box drawing characters
    ascii_matches = re.findall(ascii_pattern, content)
    if len(ascii_matches) >= 3:
        validation.results.append(ValidationResult(
            check_name="ascii_diagrams",
            passed=True,
            details=f"{len(ascii_matches)} ASCII diagram elements found"
        ))
    else:
        validation.results.append(ValidationResult(
            check_name="ascii_diagrams",
            passed=False,
            details=f"Only {len(ascii_matches)} ASCII diagram elements (need ≥3)",
            severity="WARNING"
        ))

    return validation


def generate_report(validations: list[PlaybookValidation]) -> str:
    """Generate a markdown validation report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "# Playbook Validation Report",
        "",
        f"> **Generated:** {now}",
        "> **Test ID:** WI-SAO-037",
        "> **Initiative:** SAO-INIT-007 (Triple-Lens Playbook Refactoring)",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Playbook | Status | Errors | Warnings |",
        "|----------|--------|--------|----------|",
    ]

    total_errors = 0
    total_warnings = 0
    all_passed = True

    for v in validations:
        status = "✅ PASS" if v.passed else "❌ FAIL"
        if not v.passed:
            all_passed = False
        total_errors += v.error_count
        total_warnings += v.warning_count
        playbook_name = Path(v.playbook_path).parent.name
        lines.append(f"| {playbook_name} | {status} | {v.error_count} | {v.warning_count} |")

    lines.extend([
        "",
        f"**Overall Status:** {'✅ ALL PASS' if all_passed else '❌ FAILURES DETECTED'}",
        f"**Total Errors:** {total_errors}",
        f"**Total Warnings:** {total_warnings}",
        "",
        "---",
        "",
        "## Detailed Results",
        "",
    ])

    for v in validations:
        playbook_name = Path(v.playbook_path).name
        skill_name = Path(v.playbook_path).parent.name
        lines.extend([
            f"### {skill_name}/{playbook_name}",
            "",
        ])

        # Group by check name
        checks_by_name: dict[str, list[ValidationResult]] = {}
        for r in v.results:
            if r.check_name not in checks_by_name:
                checks_by_name[r.check_name] = []
            checks_by_name[r.check_name].append(r)

        for check_name, results in checks_by_name.items():
            passed_count = sum(1 for r in results if r.passed)
            total_count = len(results)
            status_icon = "✅" if passed_count == total_count else "❌"

            lines.append(f"**{check_name}:** {status_icon} ({passed_count}/{total_count})")

            for r in results:
                if not r.passed:
                    line_info = f" (line {r.line_number})" if r.line_number else ""
                    severity_icon = "🔴" if r.severity == "ERROR" else "🟡"
                    lines.append(f"  - {severity_icon} {r.details}{line_info}")
                elif r.severity == "INFO":
                    lines.append(f"  - ℹ️ {r.details}")

            lines.append("")

    lines.extend([
        "---",
        "",
        "## Validation Checks Performed",
        "",
        "| Check | Description |",
        "|-------|-------------|",
        "| version_header | Semantic version present (X.Y.Z) |",
        "| section_L0 | L0 (ELI5) section present |",
        "| section_L1 | L1 (Engineer) section present |",
        "| section_L2 | L2 (Architect) section present |",
        "| yaml_syntax | YAML code blocks are syntactically valid |",
        "| placeholder_text | No TODO/TBD/FIXME placeholders remain |",
        "| file_reference | Referenced files exist |",
        "| antipattern_coverage | ≥3 anti-patterns documented |",
        "| ascii_diagrams | ASCII diagrams present |",
        "",
        "---",
        "",
        "*Generated by validate_playbooks.py*",
        "*Part of WI-SAO-037: Validate all examples executable*",
    ])

    return '\n'.join(lines)


def main():
    """Main entry point."""
    # Find playbooks
    base_path = Path(__file__).parent.parent.parent.parent.parent / "skills"

    playbooks = [
        base_path / "orchestration" / "PLAYBOOK.md",
        base_path / "problem-solving" / "PLAYBOOK.md",
        base_path / "nasa-se" / "PLAYBOOK.md",
    ]

    print("=" * 60)
    print("PLAYBOOK VALIDATION TEST HARNESS")
    print("WI-SAO-037: Validate all examples executable")
    print("=" * 60)
    print()

    validations = []

    for playbook_path in playbooks:
        print(f"Validating: {playbook_path.parent.name}/{playbook_path.name}")

        if not playbook_path.exists():
            print("  ❌ File not found!")
            validations.append(PlaybookValidation(
                playbook_path=str(playbook_path),
                results=[ValidationResult(
                    check_name="file_exists",
                    passed=False,
                    details="File not found",
                    severity="ERROR"
                )]
            ))
            continue

        validation = validate_playbook(playbook_path)
        validations.append(validation)

        status = "✅ PASS" if validation.passed else "❌ FAIL"
        print(f"  {status} ({validation.error_count} errors, {validation.warning_count} warnings)")

    print()
    print("=" * 60)

    # Generate report
    report = generate_report(validations)

    # Write report
    report_path = Path(__file__).parent / "VALIDATION-REPORT.md"
    report_path.write_text(report)
    print(f"Report written to: {report_path}")

    # Exit with error code if any failures
    all_passed = all(v.passed for v in validations)
    print()
    print(f"Overall: {'✅ ALL PASS' if all_passed else '❌ FAILURES DETECTED'}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
