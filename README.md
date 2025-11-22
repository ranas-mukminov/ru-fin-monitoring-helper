# 🛡️ RU Financial Monitoring Helper

![CI](https://github.com/ranas-mukminov/ru-fin-monitoring-helper/workflows/CI/badge.svg)
![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)

🇬🇧 English | 🇷🇺 [Русская версия](README.ru.md)

## Overview

RU Financial Monitoring Helper is a comprehensive starter kit for implementing financial monitoring (FinMon/AML) observability in Russian fintech, payment, and crypto platforms. It provides production-ready YAML schemas for logging authentication, KYC, transaction, and sanctions-screening events, along with preconfigured ELK/Loki pipelines, Grafana dashboards, and deterministic AI assistants for generating event sets and compliance playbooks. Designed for DevSecOps teams, this toolkit focuses on the technical implementation layer—covering what to log, how to pipeline it, and how to visualize financial monitoring events—without replacing legal or compliance guidance.

## Key Features

- **Event schemas** — YAML definitions for core FinMon event types: authentication, KYC lifecycle, transactions, AML flags, sanctions screening, and case management
- **Pipeline templates** — Ready-to-use Logstash and Loki configurations for ingesting and indexing financial events
- **Grafana dashboards** — Prebuilt monitoring dashboards for financial operations and AML activity tracking
- **Sanctions integration stubs** — Client interfaces for OpenSanctions and Sanctions Network (API-key-free examples)
- **CLI tooling** — Validate schemas, generate pipeline configurations, and scaffold compliance artifacts
- **AI-assisted helpers** — Deterministic event set suggestions and playbook drafting based on product profiles (offline, no external API calls by default)
- **Russian market focus** — Tailored to Russian regulatory environment (115-FZ, FinMon rules) while maintaining vendor-neutral architecture
- **TDD-first approach** — Comprehensive test coverage with pytest, linting, and security scanning

## Architecture / Components

The project follows a modular structure:

```
┌─────────────────┐
│ CLI Commands    │ ← Schema validation, pipeline generation, AI helpers
└────────┬────────┘
         │
    ┌────┴─────────────────────────────────┐
    │                                       │
┌───▼──────────┐                   ┌───────▼────────┐
│ Event Schemas│                   │ AI Helpers     │
│ (YAML)       │                   │ (offline)      │
└──────┬───────┘                   └────────────────┘
       │
       │ feeds into
       │
┌──────▼───────────────────────────────────┐
│ Pipelines (ELK/Loki)                     │
│ ├─ Logstash configs                      │
│ └─ Loki label extractors                 │
└──────┬───────────────────────────────────┘
       │
       │ visualized by
       │
┌──────▼───────────────────────────────────┐
│ Grafana Dashboards                       │
│ ├─ Auth/Session monitoring               │
│ ├─ Transaction volumes                   │
│ └─ AML flags & suspicious activity       │
└──────────────────────────────────────────┘
```

External integrations (sanctions lists) are abstracted via client interfaces—no production API keys included.

## Requirements

### System Requirements

- **OS**: Linux (Ubuntu 20.04+, Debian 11+, RHEL 8+, Rocky Linux 8+)
- **Python**: 3.10 or higher
- **Memory**: 2GB+ RAM for development; 8GB+ recommended for ELK stack
- **Disk**: 5GB+ for codebase and logs; 50GB+ for Elasticsearch data
- **Network**: Internet access for downloading dependencies and Docker images

### Software Dependencies

- `pip` and `virtualenv` (or `venv`)
- Docker and Docker Compose (for running ELK/Loki/Grafana examples)
- Git

### Access Requirements

- Standard user with `sudo` access (for Docker operations)
- No root required for CLI tools

## Quick Start (TL;DR)

```bash
# 1. Clone the repository
git clone https://github.com/ranas-mukminov/ru-fin-monitoring-helper.git
cd ru-fin-monitoring-helper

# 2. Install the package
pip install -e .[dev]

# 3. Validate event schemas
ru-fin-helper validate-schema --file schemas/events/transaction_core.yaml

# 4. Generate event suggestions for your product
ru-fin-helper suggest-events \
  --product examples/products/simple_psp_ru.yaml \
  --out /tmp/suggested_events.yaml

# 5. Launch ELK stack for testing
docker compose -f examples/elk/docker-compose.elk-example.yml up -d

# 6. Access Kibana at http://localhost:5601
```

## Detailed Installation

### Install on Ubuntu / Debian

```bash
# Update package index
sudo apt update

# Install Python 3.10+ and pip
sudo apt install -y python3 python3-pip python3-venv git

# Clone the repository
git clone https://github.com/ranas-mukminov/ru-fin-monitoring-helper.git
cd ru-fin-monitoring-helper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install package with dev dependencies
pip install -e .[dev]

# Verify installation
ru-fin-helper --help
```

### Install on RHEL / Rocky / Alma

```bash
# Install Python 3.10+ (may require EPEL or AppStream module)
sudo dnf install -y python3.10 python3-pip git

# Clone repository
git clone https://github.com/ranas-mukminov/ru-fin-monitoring-helper.git
cd ru-fin-monitoring-helper

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install package
pip install -e .[dev]

# Verify
ru-fin-helper --help
```

### Install with Docker (ELK/Loki Examples)

```bash
# Install Docker and Docker Compose (Ubuntu example)
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker

# Start ELK stack
cd examples/elk
docker compose -f docker-compose.elk-example.yml up -d

# Or start Loki stack
cd examples/loki
docker compose -f docker-compose.loki-example.yml up -d
```

## Configuration

### Event Schema Format

Event schemas are defined in YAML under `schemas/events/`. Example structure:

```yaml
event_name: transaction_core
description_ru: "Основные этапы платежной транзакции"
category: transaction
criticality: high
use_cases:
  - aml
  - fraud_detection
  - audit
fields:
  - name: event_type
    type: keyword
    required: true
    description: "Event type identifier"
  - name: ts
    type: datetime
    required: true
    description: "Event timestamp"
  - name: transaction_id
    type: keyword
    required: true
    description: "Unique transaction ID"
  - name: amount
    type: float
    required: true
    description: "Transaction amount"
  - name: currency
    type: keyword
    required: true
    description: "Currency code (RUB, USD, etc.)"
```

### Product Profile Format

Define your product characteristics in `examples/products/`:

```yaml
product_type: psp
channels:
  - web
  - api
geography: RU
features:
  - cards
  - merchants
description: "Russian payment gateway (PSP) example."
```

### Pipeline Configuration

ELK Logstash pipeline example (`pipelines/elk/logstash_finmon_pipeline.conf`):

```ruby
input {
  beats {
    port => 5044
  }
}

filter {
  json {
    source => "message"
  }
  
  if [event_type] == "transaction_core" {
    mutate {
      add_tag => ["finmon", "transaction"]
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "finmon-%{+YYYY.MM.dd}"
  }
}
```

### Environment Variables

No environment variables required for basic CLI usage. For production integrations:

- `OPENSANCTIONS_API_KEY` — OpenSanctions API key (optional, for sanctions screening)
- `SANCTIONS_NETWORK_TOKEN` — Sanctions Network token (optional)
- `ELK_HOST` — Elasticsearch endpoint for custom deployments
- `GRAFANA_URL` — Grafana instance URL

## Usage & Common Tasks

### Validate Event Schemas

```bash
# Validate single schema
ru-fin-helper validate-schema --file schemas/events/auth_login.yaml

# Validate all schemas in directory
for schema in schemas/events/*.yaml; do
  ru-fin-helper validate-schema --file "$schema"
done
```

### Generate Pipeline Stubs

```bash
# Generate Logstash pipeline from schema
ru-fin-helper generate-pipeline-stub \
  --schema schemas/events/transaction_core.yaml \
  --target elk \
  --out /tmp/transaction_pipeline.conf

# Generate Loki pipeline
ru-fin-helper generate-pipeline-stub \
  --schema schemas/events/kyc_lifecycle.yaml \
  --target loki \
  --out /tmp/kyc_loki_config.yaml
```

### AI-Assisted Event Suggestions

```bash
# Suggest minimal event set for a product
ru-fin-helper suggest-events \
  --product examples/products/simple_psp_ru.yaml \
  --out /tmp/suggested_events.yaml

# Review suggested events
cat /tmp/suggested_events.yaml
```

### Generate Compliance Playbooks

```bash
# Generate playbooks for a product profile
ru-fin-helper generate-playbooks \
  --product examples/products/simple_psp_ru.yaml \
  --events schemas/events/ \
  --out /tmp/playbooks/ \
  --risk-level high
```

### Access Web Interfaces

After starting Docker Compose stacks:

- **Kibana (ELK)**: http://localhost:5601
- **Grafana (Loki)**: http://localhost:3000 (default credentials: admin/admin)
- **Elasticsearch API**: http://localhost:9200

### Import Grafana Dashboards

```bash
# Copy dashboard JSON to Grafana container
docker cp dashboards/grafana/finmon_overview.json \
  <grafana_container_id>:/tmp/

# Or import via Grafana UI:
# Settings → Data Sources → Add Elasticsearch
# Dashboards → Import → Upload JSON
```

## Update / Upgrade

### Update from Git

```bash
# Navigate to repository
cd ru-fin-monitoring-helper

# Pull latest changes
git pull origin main

# Reinstall package
pip install -e .[dev]

# Run tests to verify
pytest tests/unit
```

### Update Docker Images

```bash
# Pull latest images
docker compose -f examples/elk/docker-compose.elk-example.yml pull

# Recreate containers
docker compose -f examples/elk/docker-compose.elk-example.yml up -d --force-recreate
```

### Schema Migration

When updating schemas, validate compatibility:

```bash
# Validate updated schema
ru-fin-helper validate-schema --file schemas/events/transaction_core.yaml

# Regenerate pipelines if schema changed
ru-fin-helper generate-pipeline-stub \
  --schema schemas/events/transaction_core.yaml \
  --target elk \
  --out pipelines/elk/transaction_pipeline.conf
```

## Logs, Monitoring, Troubleshooting

### View Logs

```bash
# Docker Compose logs
docker compose -f examples/elk/docker-compose.elk-example.yml logs -f

# Specific service logs
docker compose logs elasticsearch
docker compose logs logstash
docker compose logs kibana

# CLI logs (increase verbosity)
ru-fin-helper --verbose validate-schema --file schemas/events/auth_login.yaml
```

### Common Issues

**Port already in use**

```bash
# Check what's using port 9200 (Elasticsearch)
sudo lsof -i :9200

# Kill process or change port in docker-compose.yml
```

**Elasticsearch won't start (insufficient memory)**

```bash
# Increase vm.max_map_count (Linux kernel limitation)
sudo sysctl -w vm.max_map_count=262144

# Make persistent
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

**No data in Grafana dashboards**

- Verify Elasticsearch data source is configured correctly
- Check index pattern matches `finmon-*`
- Ensure logs are being ingested via Logstash (check Logstash logs)
- Test Elasticsearch query: `curl http://localhost:9200/finmon-*/_count`

**Schema validation fails**

```bash
# Check YAML syntax
yamllint schemas/events/transaction_core.yaml

# Review error messages for missing required fields
ru-fin-helper validate-schema --file schemas/events/transaction_core.yaml
```

**Permission denied (Docker)**

```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

## Security Notes

### Production Deployment Checklist

- **Change default passwords** — Elasticsearch, Kibana, Grafana all ship with default credentials. Change immediately.
- **Enable TLS/SSL** — Configure HTTPS for Elasticsearch, Kibana, Grafana in production.
- **Restrict network access** — Use firewall rules (iptables/ufw) to limit access to monitoring ports (9200, 5601, 3000).
- **VPN/bastion access** — Do not expose Kibana/Grafana directly to the Internet; use VPN or SSH tunneling.
- **API key rotation** — If using sanctions APIs, rotate keys regularly and store in secrets manager.
- **Data retention policies** — Configure index lifecycle management in Elasticsearch to avoid unbounded storage growth.
- **PII sanitization** — Mask or hash sensitive fields (user IDs, amounts) in logs before indexing.
- **Audit logging** — Enable audit logs for Elasticsearch and Grafana access.

### Compliance Considerations

- This toolkit provides technical infrastructure only; consult legal and compliance teams for regulatory requirements.
- Do not commit real API keys, production configs, or personal data to version control.
- Sanctions screening functionality is a stub; real-world deployment requires licensed data sources and legal review.

## Project Structure

```
ru-fin-monitoring-helper/
├─ cli/                         # CLI application
│  ├─ commands/                 # Command implementations
│  │  ├─ validate_schema.py
│  │  ├─ generate_pipeline_stub.py
│  │  ├─ suggest_events.py
│  │  └─ generate_playbooks.py
│  └─ main.py                   # CLI entry point
├─ schemas/                     # Event schema definitions
│  ├─ events/                   # Core event schemas (YAML)
│  │  ├─ auth_login.yaml
│  │  ├─ kyc_lifecycle.yaml
│  │  ├─ transaction_core.yaml
│  │  ├─ sanctions_screening.yaml
│  │  └─ ...
│  ├─ pipelines/                # Pipeline schema definitions
│  └─ reference/                # Reference data schemas
├─ pipelines/                   # Pipeline configuration templates
│  ├─ elk/                      # Logstash configs
│  └─ loki/                     # Loki configs
├─ dashboards/                  # Grafana dashboard definitions
│  └─ grafana/                  # JSON dashboard exports
├─ ai/                          # AI helper modules
│  └─ src/ru_fin_ai_helper/     # Event suggester, playbook generator
├─ sanctions/                   # Sanctions client stubs
│  ├─ opensanctions_client/     # OpenSanctions integration
│  └─ sanctions_network_client/ # Sanctions Network integration
├─ examples/                    # Usage examples
│  ├─ products/                 # Sample product profiles
│  ├─ logs/                     # Sample log files
│  ├─ playbooks/                # Example playbooks
│  ├─ elk/                      # ELK Docker Compose setup
│  └─ loki/                     # Loki Docker Compose setup
├─ tests/                       # Test suite
│  ├─ unit/                     # Unit tests
│  └─ integration/              # Integration tests
├─ scripts/                     # Development scripts
│  ├─ lint.sh                   # Linting
│  ├─ security_scan.sh          # Security checks
│  └─ dev_run_all_tests.sh      # Full test suite
├─ pyproject.toml               # Package metadata
├─ LEGAL.md                     # Legal disclaimer
├─ CONTRIBUTING.md              # Contribution guidelines
└─ LICENSE                      # Apache-2.0 license
```

## Roadmap / Plans

- [ ] Add more event schemas (crypto withdrawals, merchant onboarding, device fingerprinting)
- [ ] Prometheus exporter for FinMon metrics
- [ ] Vector.dev pipeline examples
- [ ] Integration with Russian cloud providers' log aggregation (Yandex Cloud Logging, VK Cloud)
- [ ] Enhanced AI playbook generator with risk scoring
- [ ] Real-time sanctions screening demo (with test data)
- [ ] Alerting rule templates for Prometheus/Grafana

## Contributing

Contributions are welcome! Please follow the **test-first** approach:

1. **Write tests first** — Add or update unit tests for validators, CLI commands, AI helpers, or sanctions clients.
2. **Implement code** — Write code to make tests pass.
3. **Run all tests** — Before committing, execute:

   ```bash
   ./scripts/dev_run_all_tests.sh
   ```

   This runs linters (ruff, mypy, yamllint) and pytest.

4. **Open a Pull Request** — Submit PR with clear description of changes.

### Code Style

- Follow PEP 8 and PEP 257
- Use type hints (mypy-compliant)
- Keep functions small and focused
- Write descriptive commit messages

### Legal Boundaries

- Do not commit real API keys, production configs, or personal data
- Respect licensing and regulatory constraints
- Use English or Russian comments where code is complex

## License

This project is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) for full text.

## Author and Commercial Support

**Author**: [Ranas Mukminov](https://github.com/ranas-mukminov)

This toolkit is developed and maintained by a DevOps/DevSecOps engineer specializing in observability and compliance infrastructure for fintech and payment platforms.

### Professional Services

For production-grade implementation, custom schema development, and ongoing support, visit **[run-as-daemon.ru](https://run-as-daemon.ru)** (Russian) or contact the author via GitHub.

Services include:

- **FinMon observability setup** — End-to-end logging, dashboards, and alerting for AML/fraud detection
- **Pipeline customization** — Tailored ELK/Loki/Vector configurations for your infrastructure
- **Compliance infrastructure audit** — Review existing systems for regulatory readiness
- **Integration with Russian cloud platforms** — Yandex Cloud, VK Cloud, other providers
- **Training and knowledge transfer** — Workshops for DevSecOps teams

---

**Disclaimer**: This project is a technical toolkit and does not constitute legal advice. It does not replace official regulatory requirements or compliance guidance. Responsibility for regulatory compliance rests with the end user. No production API keys, real sanctions lists, or personal data are included in this repository.
