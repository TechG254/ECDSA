"""
This program verifies ECDSA signatures for given messages using a public key.
It uses the pycryptodome library (Crypto module) for ECC and DSS operations.

Author: Harvester Okumu
Date: 2026-02-14
"""

from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

def verify_signature(public_key, message, signature):
    """
    Verifies an ECDSA signature for a given message and public key.

    Args:
        public_key (ECC.EccKey): The public ECC key for verification.
        message (bytes): The message in binary format.
        signature (bytes): The ECDSA signature in binary format.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    try:
        # Hash the message using SHA-256
        h = SHA256.new(message)
        # Create a verifier in 'fips-186-3' mode
        verifier = DSS.new(public_key, 'fips-186-3')
        # Verify the signature
        verifier.verify(h, signature)
        return True
    except ValueError:
        # Signature verification failed
        return False

def main():
    """
    Main program to load keys, messages, signatures and verify them.
    """
    # Load the public key from PEM file
    with open('public_key.pem', 'rt') as f:
        public_key = ECC.import_key(f.read())

    # Load messages and signatures in binary mode
    with open('message1.bin', 'rb') as f:
        message1 = f.read()
    with open('message2.bin', 'rb') as f:
        message2 = f.read()
    with open('signature1.bin', 'rb') as f:
        signature1 = f.read()
    with open('signature2.bin', 'rb') as f:
        signature2 = f.read()

    # Verify all combinations of messages and signatures
    results = [
        ("message1 & signature1", verify_signature(public_key, message1, signature1)),
        ("message1 & signature2", verify_signature(public_key, message1, signature2)),
        ("message2 & signature1", verify_signature(public_key, message2, signature1)),
        ("message2 & signature2", verify_signature(public_key, message2, signature2)),
    ]

    # Print the verification results
    print("ECDSA Signature Verification Results:\n")
    for description, result in results:
        print(f"{description}: {'Valid' if result else 'Invalid'}")

if __name__ == "__main__":
    main()
