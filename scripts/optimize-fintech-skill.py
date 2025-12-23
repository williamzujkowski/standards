#!/usr/bin/env python3
"""Aggressively optimize fintech skill to meet 5K token budget."""

import re
from pathlib import Path

skill_file = Path("skills/compliance/fintech/SKILL.md")
reference_file = Path("skills/compliance/fintech/REFERENCE.md")

content = skill_file.read_text()

# Extract detailed requirement sections (Requirements 1-12)
detailed_reqs = re.findall(r"(#### Requirement \d+:.*?)(?=#### Requirement \d+:|### Cardholder|$)", content, re.DOTALL)

# Create condensed version with just headers
condensed_requirements = """#### PCI-DSS v4.0.1 Requirements Summary

> **📚 Complete Requirements**: See [REFERENCE.md](./REFERENCE.md) for detailed sub-requirements, implementation guidance, and compliance validation procedures.

**Requirements 1-12 Overview:**

1. **Network Security Controls**: Firewalls, NSCs, CDE isolation
2. **Secure Configurations**: Vendor defaults changed, unnecessary services disabled
3. **Protect Stored Data**: Encryption at rest, minimize data retention, never store SAD
4. **Protect Data in Transit**: TLS 1.2+, strong cryptography for all PAN transmission
5. **Malware Protection**: Anti-malware on all systems, kept current, monitored
6. **Secure Development**: Threat modeling, secure coding, vulnerability management
7. **Access Control**: Least privilege, unique IDs, business need-to-know
8. **Identification & Authentication**: MFA for CDE access, strong passwords, credential management
9. **Physical Security**: Restricted facility access, badge systems, visitor logs
10. **Logging & Monitoring**: Audit trails, centralized logging, 90+ day retention
11. **Security Testing**: Quarterly vulnerability scans, annual penetration testing
12. **Security Policy**: Documented policies, awareness training, incident response

*Each requirement contains multiple sub-requirements - see REFERENCE.md for complete compliance checklist.*

"""

# Replace the detailed requirements section
pattern = r"#### Requirement 1:.*?(?=### Cardholder)"
content = re.sub(pattern, condensed_requirements, content, flags=re.DOTALL)

# Write optimized SKILL.md
skill_file.write_text(content)

# Create REFERENCE.md with detailed requirements
if detailed_reqs:
    reference_content = """# FinTech Compliance - Reference Implementation

This document contains detailed PCI-DSS v4.0.1 requirements, SOC2 control mappings, and complete implementation examples.

## Table of Contents

- [PCI-DSS v4.0.1 Detailed Requirements](#pci-dss-v401-detailed-requirements)
- [Implementation Examples](#implementation-examples)
- [Compliance Checklists](#compliance-checklists)

---

## PCI-DSS v4.0.1 Detailed Requirements

"""

    for req in detailed_reqs:
        reference_content += req + "\n\n"

    reference_content += """
---

## Implementation Examples

See main SKILL.md for essential implementation patterns.

### Network Segmentation Example

```yaml
# CDE Network Segmentation
zones:
  - name: CDE
    subnets:
      - 10.0.1.0/24  # Payment processing
      - 10.0.2.0/24  # Database servers
    firewall_rules:
      - allow: HTTPS from trusted_apps
      - allow: PostgreSQL from app_servers
      - deny: all other traffic

  - name: trusted
    subnets:
      - 10.0.10.0/24  # Application servers
    firewall_rules:
      - allow: HTTPS to CDE
      - allow: outbound to internet (whitelist)

  - name: untrusted
    subnets:
      - 10.0.20.0/24  # DMZ
    firewall_rules:
      - deny: all to CDE (no direct access)
```

### Tokenization Implementation

```python
import stripe
from typing import Dict

class PaymentTokenizer:
    \"\"\"PCI-compliant payment tokenization using Stripe.\"\"\"

    def __init__(self, api_key: str):
        stripe.api_key = api_key

    def tokenize_card(self, card_data: Dict) -> str:
        \"\"\"Convert PAN to token (never store raw PAN).\"\"\"
        token = stripe.Token.create(
            card={
                'number': card_data['number'],
                'exp_month': card_data['exp_month'],
                'exp_year': card_data['exp_year'],
                'cvc': card_data['cvc']  # Not stored after tokenization
            }
        )

        # Store only the token, not the PAN
        return token.id

    def charge_token(self, token: str, amount: int) -> Dict:
        \"\"\"Process payment using token.\"\"\"
        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            source=token,
            description='Order payment'
        )

        return {
            'transaction_id': charge.id,
            'status': charge.status,
            'last4': charge.source.last4  # Safe to store
        }
```

### Audit Evidence Collection

```python
import boto3
from datetime import datetime, timedelta
from typing import List, Dict

class ComplianceEvidenceCollector:
    \"\"\"Automated PCI compliance evidence collection.\"\"\"

    def __init__(self):
        self.s3 = boto3.client('s3')
        self.config = boto3.client('config')
        self.iam = boto3.client('iam')

    def collect_quarterly_evidence(self) -> Dict:
        \"\"\"Collect evidence for quarterly compliance review.\"\"\"
        evidence = {
            'collection_date': datetime.utcnow().isoformat(),
            'access_reviews': self._collect_access_reviews(),
            'vulnerability_scans': self._collect_vulnerability_scans(),
            'log_retention': self._verify_log_retention(),
            'mfa_status': self._verify_mfa_enforcement(),
            'encryption_configs': self._verify_encryption()
        }

        # Store evidence in secure S3 bucket
        self._store_evidence(evidence)

        return evidence

    def _collect_access_reviews(self) -> List[Dict]:
        \"\"\"Verify quarterly access reviews completed.\"\"\"
        # Retrieve IAM user last access data
        users = self.iam.list_users()['Users']

        return [{
            'username': user['UserName'],
            'created': user['CreateDate'].isoformat(),
            'last_used': self.iam.get_user(UserName=user['UserName'])
                .get('User', {}).get('PasswordLastUsed', 'Never').isoformat()
                if hasattr(self.iam.get_user(UserName=user['UserName'])
                    .get('User', {}).get('PasswordLastUsed', 'Never'), 'isoformat')
                else 'Never'
        } for user in users]

    def _collect_vulnerability_scans(self) -> Dict:
        \"\"\"Collect quarterly vulnerability scan reports.\"\"\"
        # Query AWS Inspector or third-party scanner
        return {
            'scan_date': datetime.utcnow().isoformat(),
            'tool': 'AWS Inspector',
            'status': 'completed'
        }

    def _verify_log_retention(self) -> Dict:
        \"\"\"Verify 90+ day log retention (PCI Req 10.5.1).\"\"\"
        logs = boto3.client('logs')
        log_groups = logs.describe_log_groups()['logGroups']

        non_compliant = [
            lg['logGroupName']
            for lg in log_groups
            if lg.get('retentionInDays', 0) < 90
        ]

        return {
            'total_log_groups': len(log_groups),
            'non_compliant': non_compliant,
            'compliant': len(non_compliant) == 0
        }

    def _verify_mfa_enforcement(self) -> Dict:
        \"\"\"Verify MFA enabled for all users with CDE access.\"\"\"
        users = self.iam.list_users()['Users']

        no_mfa = [
            user['UserName']
            for user in users
            if not self.iam.list_mfa_devices(UserName=user['UserName'])['MFADevices']
        ]

        return {
            'total_users': len(users),
            'users_without_mfa': no_mfa,
            'mfa_compliance': len(no_mfa) == 0
        }

    def _verify_encryption(self) -> Dict:
        \"\"\"Verify encryption at rest and in transit.\"\"\"
        return {
            's3_encryption': 'AES-256',
            'rds_encryption': 'enabled',
            'tls_version': 'TLS 1.2+'
        }

    def _store_evidence(self, evidence: Dict):
        \"\"\"Store evidence in compliance bucket.\"\"\"
        bucket = 'compliance-evidence-bucket'
        key = f\"quarterly/{datetime.utcnow().strftime('%Y-%m')}/evidence.json\"

        self.s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(evidence, indent=2),
            ServerSideEncryption='AES256'
        )
```

---

## Compliance Checklists

### PCI-DSS SAQ A (E-commerce)

- [ ] Merchant only uses approved payment processors (no CDE)
- [ ] PCI DSS compliant service provider confirmed
- [ ] SSL/TLS certificates valid and current
- [ ] Payment pages use HTTPS
- [ ] No storage of cardholder data
- [ ] Quarterly vulnerability scans completed
- [ ] Annual security awareness training completed

### PCI-DSS SAQ D (Full scope)

- [ ] All 12 requirements fully implemented
- [ ] Quarterly internal vulnerability scans
- [ ] Quarterly external ASV scans (passing)
- [ ] Annual penetration testing
- [ ] Annual audit (Level 1 merchants)
- [ ] Quarterly compliance reviews
- [ ] Incident response plan tested
- [ ] Network segmentation verified

### SOC2 Type II Readiness

- [ ] All Trust Service Criteria controls documented
- [ ] 6-12 month observation period completed
- [ ] Evidence collection automated
- [ ] Control testing performed
- [ ] Exceptions remediated
- [ ] Auditor selected
- [ ] Management representation letter prepared

---

## Additional Resources

- [PCI Security Standards Council](https://www.pcisecuritystandards.org)
- [AICPA SOC2 Resources](https://www.aicpa.org/soc)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
"""

    reference_file.write_text(reference_content)
    print(f"✅ Created REFERENCE.md ({len(reference_content):,} chars)")

# Calculate new token count
new_content = skill_file.read_text()
level2_match = re.search(r"## Level 2:(.*?)(?=## Level 3:|$)", new_content, re.DOTALL)
if level2_match:
    level2_new = level2_match.group(1)
    new_tokens = len(level2_new) // 4
    original_tokens = 6132
    reduction = original_tokens - new_tokens

    print("✅ Optimized SKILL.md")
    print(f"   Original: {original_tokens:,} tokens")
    print(f"   New: {new_tokens:,} tokens")
    print(f"   Reduction: {reduction:,} tokens ({reduction/original_tokens*100:.1f}%)")
    print(f"   Status: {'✅ Compliant' if new_tokens < 5000 else '⚠️ Still over budget'}")
