---
title: "NIST AI RMF Generative AI Profile"
status: "authoritative-summary"
owner: "@williamzujkowski"
source:
  url: "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf"
  retrieved: "2025-08-22"
review:
  last_reviewed: "2025-08-22"
  next_review_due: "2026-02-22"
accuracy: "verified"
---

# NIST AI RMF Generative AI Profile (NIST.AI.600-1)

## Overview

The NIST Generative AI Profile (GAI-P 1.0) extends the AI RMF to address unique risks associated with generative AI systems. Published as NIST.AI.600-1, it provides specific guidance for managing risks from models that generate content including text, images, audio, video, and code.

## Generative AI-Specific Risks

### Content Authenticity Risks

- **Misinformation and Disinformation**: False or misleading generated content
- **Deepfakes**: Synthetic media impersonating real individuals
- **Content Provenance**: Inability to verify content origin

### Technical Risks

- **Confabulation/Hallucination**: Generation of plausible but false information
- **Data Privacy**: Training data memorization and extraction
- **Prompt Injection**: Malicious manipulation of model behavior
- **Model Inversion**: Extracting training data from models

### Societal Risks

- **Harmful Bias Amplification**: Perpetuation of societal biases
- **Environmental Impact**: High computational resource consumption
- **Intellectual Property**: Copyright and attribution concerns

## GAI-Specific Actions by Function

### GOVERN

Organizations MUST:

- Establish GAI-specific policies
- Define acceptable use policies
- Implement content moderation strategies
- Create disclosure requirements

### MAP

Organizations MUST:

- Identify GAI system capabilities and limitations
- Document intended use cases
- Map potential misuse scenarios
- Assess downstream impact

### MEASURE

Organizations SHOULD:

- Test for hallucination rates
- Evaluate bias in generated content
- Measure factual accuracy
- Assess content authenticity

### MANAGE

Organizations MUST:

- Implement content filtering
- Deploy watermarking/provenance
- Monitor for misuse
- Maintain human oversight

## Key Safeguards

### Pre-Deployment

- Red team testing for harmful outputs
- Robustness testing against adversarial inputs
- Bias and fairness assessments
- Safety evaluations

### Post-Deployment

- Content moderation systems
- User feedback mechanisms
- Incident response procedures
- Continuous monitoring

## Implementation Requirements

Organizations deploying generative AI MUST:

- Disclose AI-generated content
- Implement content authentication
- Provide opt-out mechanisms where appropriate
- Maintain audit trails

Organizations SHOULD:

- Use constitutional AI principles
- Implement retrieval-augmented generation (RAG)
- Deploy guardrails and filters
- Conduct regular audits

## References

- **Primary Source**: [NIST.AI.600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- **Parent Framework**: [NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
- **NIST GenAI Program**: [nist.gov/artificial-intelligence/generative-ai](https://www.nist.gov/artificial-intelligence/generative-ai)
