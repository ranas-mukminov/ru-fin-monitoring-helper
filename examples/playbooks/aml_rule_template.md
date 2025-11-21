# AML Rule Template

- **Rule ID:** RULE-001
- **Description:** Trigger manual review for high-risk country transfers > 100000 RUB/day.
- **Data needed:** transaction_core, transaction_aml_flags, sanctions_screening.
- **Actions:** block, escalate to finmon, open case in case_management.
