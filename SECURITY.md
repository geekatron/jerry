# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest release | Yes |
| Older releases | No |

Only the latest release receives security updates. We recommend always running the most recent version.

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them using [GitHub's private vulnerability reporting](https://github.com/geekatron/jerry/security/advisories/new).

When reporting, please include:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if any)

### What to Expect

- **Acknowledgment:** Within 48 hours of your report
- **Status update:** Within 7 days with an initial assessment
- **Resolution:** We aim to address confirmed vulnerabilities within 30 days

### Scope

The following are in scope for security reports:

- Command injection via hook scripts
- Arbitrary code execution through plugin mechanisms
- Credential or secret exposure in outputs
- Path traversal vulnerabilities

### Out of Scope

- Issues in upstream dependencies (report to the relevant project)
- Social engineering attacks
- Denial of service attacks

## Security Best Practices for Users

- Keep your Jerry installation up to date
- Review hook scripts before enabling them
- Do not commit `.env` files or credentials to repositories using Jerry
- Use environment variables for sensitive configuration
