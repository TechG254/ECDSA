"""
This script demonstrates how to:
1. Generate ECDSA keys (P-256 curve)
2. Create messages and signatures
3. Save keys, messages, and signatures to files
4. Verify signatures using the public key

Files generated:
- private_key.pem      : ECDSA private key
- public_key.pem       : ECDSA public key
- message1.bin, message2.bin : messages
- signature1.bin, signature2.bin : signatures

Author: Harvester Okumu
Date: 2026-02-14
"""

from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import os

# ------------------------------
# Step 1: Key Generation
# ------------------------------
def generate_ecdsa_keys(private_file="private_key.pem", public_file="public_key.pem"):
    """
    Generates an ECDSA key pair and saves them to files.
    """
    key = ECC.generate(curve='P-256')
    
    # Save private key
    with open(private_file, "wt") as f:
        f.write(key.export_key(format='PEM'))
    
    # Save public key
    with open(public_file, "wt") as f:
        f.write(key.public_key().export_key(format='PEM'))
    
    print(f"Keys saved: {private_file}, {public_file}")
    return key, key.public_key()

# ------------------------------
# Step 2: Create Messages & Signatures
# ------------------------------
def create_messages_and_signatures(private_key, messages, signature_files):
    """
    Signs each message with the private key and saves messages and signatures to files.
    """
    signer = DSS.new(private_key, 'fips-186-3')

    for i, message in enumerate(messages):
        # Hash message
        h = SHA256.new(message)
        # Sign message
        signature = signer.sign(h)
        # Save message
        with open(f"message{i+1}.bin", "wb") as f:
            f.write(message)
        # Save signature
        with open(signature_files[i], "wb") as f:
            f.write(signature)
        print(f"Saved message{i+1}.bin and {signature_files[i]}")

# ------------------------------
# Step 3: Signature Verification
# ------------------------------
def verify_signature(public_key, message, signature):
    """
    Verifies an ECDSA signature.
    Returns True if valid, False otherwise.
    """
    try:
        h = SHA256.new(message)
        verifier = DSS.new(public_key, 'fips-186-3')
        verifier.verify(h, signature)
        return True
    except ValueError:
        return False

# ------------------------------
# Step 4: Main Program
# ------------------------------
def main():
    # Check if keys exist, else generate
    if not os.path.exists("private_key.pem") or not os.path.exists("public_key.pem"):
        private_key, public_key = generate_ecdsa_keys()
    else:
        # Load keys from files
        with open("private_key.pem", "rt") as f:
            private_key = ECC.import_key(f.read())
        with open("public_key.pem", "rt") as f:
            public_key = ECC.import_key(f.read())

    # Example messages
    messages = [
        b"Hello, this is message 1",
        b"Hello, this is message 2"
    ]
    signature_files = ["signature1.bin", "signature2.bin"]

    # Create messages and signatures if they don't exist
    for m_file, s_file in zip(["message1.bin", "message2.bin"], signature_files):
        if not os.path.exists(m_file) or not os.path.exists(s_file):
            create_messages_and_signatures(private_key, messages, signature_files)
            break  # only need to generate once

    # Load messages and signatures
    message1 = open("message1.bin", "rb").read()
    message2 = open("message2.bin", "rb").read()
    signature1 = open("signature1.bin", "rb").read()
    signature2 = open("signature2.bin", "rb").read()

    # Test all combinations of messages and signatures
    tests = [
        ("message1 + signature1", message1, signature1),
        ("message1 + signature2", message1, signature2),
        ("message2 + signature1", message2, signature1),
        ("message2 + signature2", message2, signature2),
    ]

    for desc, msg, sig in tests:
        result = verify_signature(public_key, msg, sig)
        print(f"{desc}: {'Valid' if result else 'Invalid'}")

if __name__ == "__main__":
    main()