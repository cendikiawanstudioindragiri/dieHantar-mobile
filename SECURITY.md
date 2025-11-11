# Security Policy

## Reporting a Vulnerability

If you believe you have found a security vulnerability, please do not open a public issue.

Instead, email: security@cendikiawanstudios.com with the details and reproduction steps. We will respond as soon as possible.

## Supported Versions

We aim to patch security issues on the `main` branch and provide guidance for stable releases if applicable.

## Handling Sensitive Information

- Never commit secrets to the repository. Use environment variables and secret managers.
- Do not log credentials or tokens. Sanitize logs and redact sensitive values.
- Rotate credentials periodically and after incidents.
