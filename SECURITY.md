# Security Policy

## Supported Versions

| Version | Supported |
| --- | --- |
| `main` | Yes |
| Latest PyPI release | Yes |
| Older releases | No |

## Reporting A Vulnerability

Please do not open public GitHub issues for security-sensitive reports.

Instead, email `andrewanjieyang@gmail.com` with:

- a short description of the issue
- affected versions or commit hashes
- reproduction steps or a proof of concept
- impact assessment if you already have one

Use the subject line `UncommonRoute security report` so it is easy to triage.

## Response Expectations

- Initial acknowledgement target: within 3 business days
- Follow-up status update target: within 7 business days
- Coordinated disclosure after a fix is ready or a mitigation is available

## Scope

Examples of issues that should be reported privately:

- remote code execution
- credential or API key disclosure
- auth bypass in proxy/admin surfaces
- arbitrary file read/write
- request smuggling or SSRF against configured upstreams
- sensitive dashboard data exposure
