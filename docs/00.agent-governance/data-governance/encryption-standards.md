# Data Encryption & Key Management Standards

---

title: Encryption & KMS Standards
version: 1.1.0
owner: Security Officer
layer: governance
stage: 00
status: active
last-updated: 2026-05-04

---

## Overview

This document defines the encryption standards and key management strategy (KMS) for securely protecting data within `Project-Template`.

## 1. Encryption Standards (Data-at-Rest)

### AES-256-GCM (Recommended)

All sensitive data must be encrypted using AES-256-GCM (Authenticated Encryption).

- **Key Size**: 256 bits.
- **Mode**: GCM (Galois/Counter Mode) — provides simultaneous confidentiality and integrity.
- **Nonce/IV**: A unique 12-byte nonce must be generated for each encryption operation and stored alongside the ciphertext.

### Implementation Example (Python)

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_data(data: bytes, key: bytes) -> bytes:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    return nonce + ciphertext
```

## 2. Key Management Strategy (KMS)

### Envelope Encryption

Use a strategy that separates the **Data Key (DK)**, which directly encrypts the data, from the **Master Key (MK)**, which encrypts that DK.

1. **Master Key**: Managed securely in AWS KMS, GCP KMS, or HashiCorp Vault — never stored locally or in source code.
2. **Data Key**: Generated per record or session; must be discarded after use or encrypted with the Master Key before storage.

### Key Rotation

- **Automatic Rotation**: Configure Master Key to rotate automatically once per year.
- **Manual Rotation**: If key exposure is suspected, immediately replace with a new key and follow the data re-encryption procedure.

## 3. Data-in-Transit (TLS)

- All external communications must enforce **TLS 1.3** or higher.
- mTLS (mutual TLS) is also recommended for internal service-to-service communication (Service Mesh).

---

## AI Execution Checklist

- [ ] **Target**: Verified encryption implementation for <data-field>.
- [ ] **Entry Gate**: Read encryption-standards.md.
- [ ] **Procedure**: Use AES-256-GCM. Implement Envelope Encryption for high-scale data.
- [ ] **Exit Gate**: Verify that keys are not logged or stored in plain text.
- [ ] **Hard Stop**: STOP if a custom encryption algorithm is proposed instead of industry standards.
