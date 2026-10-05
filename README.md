# kestrel-pay

Kestrel Pay: merchant payment processing API and platform.

## Overview

This repository contains the core payment processing service for Kestrel Commerce. It handles payment authorization, settlement, and merchant account management.

**Important:** This is a demo/scaffold repository for local development and testing. All sample code is fictional. No real network calls or payment processing occur without explicit configuration.

## Project Links

- **Jira Project:** [Configure Jira project link]
- **Jira Service:** [Configure operations/incident tracking project]
- **Documentation:** [Configure documentation link]
- **Service Owners:** Payments Engineering team

## Structure

```
kestrel-pay/
├── src/
│   ├── payment_processor.py    # Payment authorization and retry logic
│   ├── gateway_config.py       # Payment gateway configuration
│   └── idempotency.py          # Idempotency key handling
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions no-op demo deployment
├── tests/
│   └── test_demo.py            # Offline standard-library unit tests
├── README.md                    # This file
└── requirements.txt            # No external dependencies
```

## Quick Start (Local Development)

### Prerequisites
- Python 3.10+ (standard library only)

### Setup

```bash
# From the local scaffold directory:
cd prototypes/kestrel-pay-repo
# No dependency install is needed; do not clone until your connected GitHub org is known.
```

### Running Locally

```bash
python src/payment_processor.py
```

Running the module prints a deterministic, local mock result; it does **not** start an HTTP server or connect to a payment gateway.

## Illustrative API contract (not implemented by this scaffold)

The functions below describe what a real Kestrel Pay HTTP service could expose. This repository contains only an offline Python simulation; it does not listen for HTTP requests.

### POST /authorize
Authorizes a payment transaction.

**Request:**
```json
{
  "merchant_id": "MERCH-7412",
  "amount_cents": 12550,
  "currency": "USD",
  "idempotency_key": "abc123def456"
}
```

**Response (Success):**
```json
{
  "transaction_id": "txn_abc123",
  "status": "authorized",
  "timestamp": "2026-10-01T10:15:32Z"
}
```

**Response (Timeout/Failure):**
```json
{
  "error": "gateway_timeout",
  "message": "Payment gateway did not respond within 10s",
  "retry_after": 2
}
```

## Deployment

### Manual Deployment

```bash
git push origin main
# GitHub Actions workflow triggers automatically
# See .github/workflows/deploy.yml for details
```

### GitHub Actions Workflow

The `deploy.yml` workflow runs offline tests and then a **no-op demo job** tied to the GitHub Actions environment `demo-production`. This creates a GitHub *demo deployment record*, not a release of an application. It does not call a payment gateway or post a deployment directly to Jira.

To get Jira-visible evidence: create the remote repository in a GitHub organization already connected through GitHub for Jira; use an actual `KCPAY-n` key in the PR, branch and commit; enable the `demo-production` environment; then push to `main` and confirm the workflow succeeds. Check whether GitHub for Jira ingests the deployment and associates it with that issue. If Jira does not show it, **do not claim a deployment is visible**; use the verified PR/commit evidence or diagnose connector permissions and indexing. A successful Actions run alone does not prove Jira ingestion.

### Integration with Jira

1. Check which GitHub organization is connected to `twc-2026` through GitHub for Jira. Create the remote repository in that organization; do not assume any example GitHub URL exists.
2. Push the scaffold only after reviewing it. Use an actual, created `KCPAY-n` key in a branch, PR title and commit message.
3. Run the workflow and verify the GitHub `demo-production` deployment record on the commit.
4. Open the matching KCPAY work item and **observe** whether PR/commit and deployment evidence appears in Jira. If it does not, check the app's access, permissions, association and indexing; do not describe a deployment as Jira-visible until it is observed.

The no-op deployment is a GitHub demo event; it is never a real production release. If the connector cannot supply a Jira-visible deployment, use the PR/commit evidence as the honest fallback.

## Configuration

### Gateway Timeout Configuration

```python
# src/gateway_config.py
GATEWAY_TIMEOUT_SECONDS = 10
RETRY_ATTEMPTS = 3
RETRY_BACKOFF_MS = 500
```

**Configuration notes:**
- Timeout is currently set to 10s
- Retry logic is configured for idempotent requests
- Changes should be tracked via Jira issue key in branch names

For demo purposes, this configuration is exemplary. In production, track timeout changes via your Jira project tracking system.

## Incident Response

### If Payment Processing Fails

1. Check the local fictional merchant dashboard for its error state.
2. Inspect the simulated console output and record the displayed correlation ID.
3. Compare the observations to the published KCENG Payment Failure Runbook.
4. If the JSM demo permissions allow it, log a synthetic incident in KCOPS. This scaffold has no Docker service or real gateway endpoint to query.

### Past Incidents

- Past incidents tracked in your incident management system
- Example: Payment gateway timeout scenarios with config changes require careful testing before deployment

## Development

### Branch Naming Convention

- Feature: `[JIRA-PROJECT]-{issue-number}-{slug}`
- Bugfix: `[JIRA-PROJECT]-{issue-number}-fix-{slug}`
- Hotfix: `hotfix/{description}`

Example: `PROJ-87-tune-gateway-timeouts`

### Code Review

- Request a review before merging the demo PR.
- Use a real KCPAY key in the branch and PR title; validate Jira's Development panel after the GitHub integration indexes it.
- Do not claim a PR was merged or deployed until those events exist in the connected repository.

### Testing

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

The offline tests require only the Python standard library. No coverage percentage is asserted.

## Demo Notes

This repository is scaffolded for demonstration purposes:

- **No real payment processing** occurs. All transactions are simulated.
- **No credentials** are stored in this repository, and the demo workflow does not require deployment secrets.
- **Deployment workflow is a no-op** by design. It creates a GitHub `demo-production` deployment record but does not release software; Jira ingestion is unverified until checked in the linked KCPAY issue.
- **Mock API responses** are hardcoded for repeatability and safety.
- **Local development** uses in-memory state; no database is required.

## Contributing

See `CONTRIBUTING.md` (not in this scaffold; would be in a real repo).

## License

Proprietary — Kestrel Commerce.
