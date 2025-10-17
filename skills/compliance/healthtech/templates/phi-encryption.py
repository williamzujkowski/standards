#!/usr/bin/env python3
"""
PHI Encryption Implementation - HIPAA Compliant
AES-256 encryption for Protected Health Information

LEGAL DISCLAIMER: This is a reference implementation for educational purposes.
Production implementations must be reviewed by security professionals and 
compliance officers. Key management and operational procedures are critical.

Requirements:
    pip install cryptography
"""

import os
import base64
import json
from typing import Dict, Any, Optional
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives.asymmetric import rsa, padding


class PHIEncryption:
    """
    HIPAA-compliant PHI encryption using AES-256-GCM
    
    Security Features:
    - AES-256-GCM for authenticated encryption
    - Unique IV (Initialization Vector) per encryption
    - PBKDF2 key derivation (if using password-based encryption)
    - Metadata preservation for audit logging
    """
    
    def __init__(self, key: Optional[bytes] = None):
        """
        Initialize PHI encryption with encryption key
        
        Args:
            key: 32-byte (256-bit) encryption key. If None, generates new key.
        """
        if key is None:
            self.key = self._generate_key()
        else:
            if len(key) != 32:
                raise ValueError("Encryption key must be 32 bytes (256 bits)")
            self.key = key
    
    @staticmethod
    def _generate_key() -> bytes:
        """Generate a new 256-bit encryption key"""
        return os.urandom(32)
    
    @staticmethod
    def derive_key_from_password(password: str, salt: Optional[bytes] = None) -> tuple:
        """
        Derive encryption key from password using PBKDF2
        
        Args:
            password: User password
            salt: Salt for key derivation (generates if None)
            
        Returns:
            Tuple of (derived_key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=600000,  # OWASP recommended minimum (2023)
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        
        return key, salt
    
    def encrypt_phi(
        self,
        phi_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Encrypt PHI data with AES-256-GCM
        
        Args:
            phi_data: Dictionary containing PHI fields to encrypt
            metadata: Optional metadata for audit logging (not encrypted)
            
        Returns:
            Dictionary with encrypted data and metadata
        """
        # Serialize PHI data to JSON
        phi_json = json.dumps(phi_data, sort_keys=True)
        phi_bytes = phi_json.encode('utf-8')
        
        # Generate unique IV (12 bytes for GCM)
        iv = os.urandom(12)
        
        # Create AES-GCM cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.GCM(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Encrypt PHI
        ciphertext = encryptor.update(phi_bytes) + encryptor.finalize()
        
        # Get authentication tag
        tag = encryptor.tag
        
        # Prepare encrypted package
        encrypted_package = {
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8'),
            'algorithm': 'AES-256-GCM',
            'encrypted_at': datetime.utcnow().isoformat() + 'Z',
            'metadata': metadata or {}
        }
        
        return encrypted_package
    
    def decrypt_phi(self, encrypted_package: Dict[str, str]) -> Dict[str, Any]:
        """
        Decrypt PHI data
        
        Args:
            encrypted_package: Dictionary from encrypt_phi()
            
        Returns:
            Decrypted PHI data as dictionary
            
        Raises:
            ValueError: If decryption or authentication fails
        """
        # Extract components
        ciphertext = base64.b64decode(encrypted_package['ciphertext'])
        iv = base64.b64decode(encrypted_package['iv'])
        tag = base64.b64decode(encrypted_package['tag'])
        
        # Verify algorithm
        if encrypted_package.get('algorithm') != 'AES-256-GCM':
            raise ValueError(f"Unsupported algorithm: {encrypted_package.get('algorithm')}")
        
        # Create AES-GCM cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.GCM(iv, tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        try:
            # Decrypt and verify authentication tag
            plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()
            plaintext = plaintext_bytes.decode('utf-8')
            
            # Parse JSON
            phi_data = json.loads(plaintext)
            
            return phi_data
        
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    def export_key(self) -> str:
        """Export encryption key as base64-encoded string"""
        return base64.b64encode(self.key).decode('utf-8')
    
    @classmethod
    def import_key(cls, key_b64: str) -> 'PHIEncryption':
        """Import encryption key from base64-encoded string"""
        key = base64.b64decode(key_b64)
        return cls(key=key)


class PHIFieldEncryption:
    """
    Field-level encryption for selective PHI protection
    Encrypts specific fields while preserving non-PHI data structure
    """
    
    def __init__(self, encryption: PHIEncryption):
        """
        Initialize field-level encryption
        
        Args:
            encryption: PHIEncryption instance
        """
        self.encryption = encryption
    
    def encrypt_fields(
        self,
        data: Dict[str, Any],
        fields_to_encrypt: list
    ) -> Dict[str, Any]:
        """
        Encrypt specified fields in data dictionary
        
        Args:
            data: Dictionary containing data
            fields_to_encrypt: List of field names to encrypt
            
        Returns:
            Dictionary with specified fields encrypted
        """
        encrypted_data = data.copy()
        
        for field in fields_to_encrypt:
            if field in encrypted_data:
                # Extract field value
                field_value = {field: encrypted_data[field]}
                
                # Encrypt field
                encrypted_field = self.encryption.encrypt_phi(
                    phi_data=field_value,
                    metadata={'field_name': field}
                )
                
                # Replace field value with encrypted package
                encrypted_data[field] = {
                    '_encrypted': True,
                    '_data': encrypted_field
                }
        
        return encrypted_data
    
    def decrypt_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decrypt encrypted fields in data dictionary
        
        Args:
            data: Dictionary with encrypted fields
            
        Returns:
            Dictionary with fields decrypted
        """
        decrypted_data = data.copy()
        
        for field, value in data.items():
            if isinstance(value, dict) and value.get('_encrypted'):
                # Decrypt field
                encrypted_package = value['_data']
                decrypted_field = self.encryption.decrypt_phi(encrypted_package)
                
                # Restore original field value
                field_name = encrypted_package['metadata']['field_name']
                decrypted_data[field] = decrypted_field[field_name]
        
        return decrypted_data


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("PHI Encryption Implementation - HIPAA Compliant")
    print("=" * 70)
    print()
    
    # Example 1: Full PHI record encryption
    print("Example 1: Full PHI Record Encryption")
    print("-" * 70)
    
    # Initialize encryption
    phi_enc = PHIEncryption()
    
    # Sample PHI data
    patient_phi = {
        'mrn': '123456789',
        'name': 'John Michael Smith',
        'dob': '1970-03-15',
        'ssn': '123-45-6789',
        'address': '123 Main Street, Apt 4B, Springfield, IL 62701',
        'phone': '(555) 123-4567',
        'email': 'john.smith@example.com',
        'diagnosis': 'Essential Hypertension (I10)',
        'medication': 'Lisinopril 10mg daily'
    }
    
    print(f"Original PHI Data: {json.dumps(patient_phi, indent=2)}")
    print()
    
    # Encrypt PHI
    encrypted_phi = phi_enc.encrypt_phi(
        phi_data=patient_phi,
        metadata={
            'patient_id': 'P123456',
            'encrypted_by': 'system',
            'purpose': 'storage'
        }
    )
    
    print(f"Encrypted PHI Package:")
    print(f"  Algorithm: {encrypted_phi['algorithm']}")
    print(f"  Encrypted At: {encrypted_phi['encrypted_at']}")
    print(f"  Ciphertext: {encrypted_phi['ciphertext'][:50]}... (truncated)")
    print(f"  IV: {encrypted_phi['iv']}")
    print(f"  Tag: {encrypted_phi['tag']}")
    print(f"  Metadata: {json.dumps(encrypted_phi['metadata'], indent=2)}")
    print()
    
    # Decrypt PHI
    decrypted_phi = phi_enc.decrypt_phi(encrypted_phi)
    print(f"Decrypted PHI Data: {json.dumps(decrypted_phi, indent=2)}")
    print()
    
    # Verify integrity
    assert patient_phi == decrypted_phi, "Decryption integrity check failed"
    print("✓ Decryption integrity verified")
    print()
    
    # Example 2: Field-level encryption
    print("Example 2: Field-Level Encryption (Selective PHI Protection)")
    print("-" * 70)
    
    # Initialize field-level encryption
    field_enc = PHIFieldEncryption(phi_enc)
    
    # Sample patient record with mixed PHI and non-PHI data
    patient_record = {
        'patient_id': 'P123456',  # Non-PHI identifier
        'visit_date': '2025-10-17',  # Non-PHI
        'mrn': '123456789',  # PHI
        'name': 'John Michael Smith',  # PHI
        'dob': '1970-03-15',  # PHI
        'ssn': '123-45-6789',  # PHI
        'vital_signs': {  # Non-PHI aggregate data
            'bp_systolic': 120,
            'bp_diastolic': 80
        }
    }
    
    # Encrypt only PHI fields
    phi_fields = ['mrn', 'name', 'dob', 'ssn']
    encrypted_record = field_enc.encrypt_fields(patient_record, phi_fields)
    
    print(f"Original Record: {json.dumps(patient_record, indent=2)}")
    print()
    print(f"Record with Encrypted PHI Fields:")
    print(f"  patient_id: {encrypted_record['patient_id']}")
    print(f"  visit_date: {encrypted_record['visit_date']}")
    print(f"  mrn: [ENCRYPTED]")
    print(f"  name: [ENCRYPTED]")
    print(f"  dob: [ENCRYPTED]")
    print(f"  ssn: [ENCRYPTED]")
    print(f"  vital_signs: {encrypted_record['vital_signs']}")
    print()
    
    # Decrypt PHI fields
    decrypted_record = field_enc.decrypt_fields(encrypted_record)
    print(f"Decrypted Record: {json.dumps(decrypted_record, indent=2)}")
    print()
    
    # Verify integrity
    assert patient_record == decrypted_record, "Field-level decryption integrity check failed"
    print("✓ Field-level decryption integrity verified")
    print()
    
    # Example 3: Password-based key derivation
    print("Example 3: Password-Based Key Derivation")
    print("-" * 70)
    
    password = "SecureP@ssw0rd!2025"
    
    # Derive key from password
    derived_key, salt = PHIEncryption.derive_key_from_password(password)
    
    print(f"Password: {password}")
    print(f"Salt: {base64.b64encode(salt).decode('utf-8')}")
    print(f"Derived Key: {base64.b64encode(derived_key).decode('utf-8')}")
    print()
    
    # Initialize encryption with derived key
    phi_enc_password = PHIEncryption(key=derived_key)
    
    # Encrypt PHI
    encrypted_phi_password = phi_enc_password.encrypt_phi(patient_phi)
    print(f"PHI encrypted with password-derived key")
    print()
    
    # Re-derive key and decrypt
    redervied_key, _ = PHIEncryption.derive_key_from_password(password, salt=salt)
    phi_enc_password_2 = PHIEncryption(key=redervied_key)
    decrypted_phi_password = phi_enc_password_2.decrypt_phi(encrypted_phi_password)
    
    assert patient_phi == decrypted_phi_password, "Password-based decryption failed"
    print("✓ Password-based encryption/decryption verified")
    print()
    
    # Example 4: Key export/import
    print("Example 4: Key Export and Import")
    print("-" * 70)
    
    # Export key
    key_b64 = phi_enc.export_key()
    print(f"Exported Key (base64): {key_b64}")
    print()
    
    # Import key
    phi_enc_imported = PHIEncryption.import_key(key_b64)
    
    # Test with imported key
    decrypted_phi_imported = phi_enc_imported.decrypt_phi(encrypted_phi)
    
    assert patient_phi == decrypted_phi_imported, "Imported key decryption failed"
    print("✓ Key export/import verified")
    print()
    
    print("=" * 70)
    print("All PHI encryption tests passed successfully!")
    print("=" * 70)
    print()
    print("IMPORTANT SECURITY NOTES:")
    print("1. Store encryption keys in a Hardware Security Module (HSM) or Key Management Service (KMS)")
    print("2. Rotate encryption keys annually minimum")
    print("3. Implement key versioning for key rotation without re-encrypting all data")
    print("4. Never hardcode encryption keys in source code")
    print("5. Use environment variables or secure configuration for key material")
    print("6. Audit all encryption/decryption operations")
    print("7. Implement role-based access control (RBAC) for encryption key access")
    print("8. Test disaster recovery procedures for key recovery")
    print()
