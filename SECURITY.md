# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| < 0.2   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **mkarots@users.noreply.github.com**

### What to Include

When reporting a vulnerability, please include:

- A description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if you have one)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution**: Depends on severity and complexity

### Security Best Practices

When using Grompt:

- **Never commit sensitive data** (API keys, tokens, etc.) to prompt files
- **Review prompt files** before committing to version control
- **Use environment variables** for sensitive configuration
- **Keep dependencies updated** (`pip install --upgrade grompt`)

### Known Security Considerations

- Grompt reads YAML files from the filesystem - ensure prompt directories are properly secured
- Template rendering uses Jinja2 - be cautious with user-provided templates
- No network access is performed by Grompt itself

## Disclosure Policy

- Security vulnerabilities will be disclosed publicly after a fix is available
- Credit will be given to reporters (unless they prefer to remain anonymous)
- A security advisory will be published on GitHub

Thank you for helping keep Grompt secure! 🔒

