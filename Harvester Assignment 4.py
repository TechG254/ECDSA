"""
ECDSA Signature Verification

This script:
1. Loads an ECDSA public key from file
2. Loads two messages and two signatures
3. Verifies all message/signature combinations
4. Prints which signatures are valid

Author: Harvester Okumu
Date: 02/19/2026
"""

from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256


# -----------------------------------
# Step 1: Verification Function
# -----------------------------------
def verify_signature(public_key, message, signature):
    """
    Verifies an ECDSA signature.

    Parameters:
        public_key : ECC public key object
        message    : message in binary format
        signature  : signature in binary format

    Returns:
        True  -> if signature is valid
        False -> if signature is invalid
    """
    try:
        # Hash the message
        h = SHA256.new(message)

        # Create verifier in FIPS 186-3 mode
        verifier = DSS.new(public_key, 'fips-186-3')

        # Verify signature
        verifier.verify(h, signature)

        return True

    except (ValueError, TypeError):
        return False


# -----------------------------------
# Step 2: Main Program
# -----------------------------------
def main():

    # Load public key
    with open("public_key.pem", "rt") as f:
        public_key = ECC.import_key(f.read())

    # Load messages (binary mode)
    with open("message1.bin", "rb") as f:
        message1 = f.read()

    with open("message2.bin", "rb") as f:
        message2 = f.read()

    # Load signatures (binary mode)
    with open("signature1.bin", "rb") as f:
        signature1 = f.read()

    with open("signature2.bin", "rb") as f:
        signature2 = f.read()

    # Test all four combinations
    tests = [
        ("message1 + signature1", message1, signature1),
        ("message1 + signature2", message1, signature2),
        ("message2 + signature1", message2, signature1),
        ("message2 + signature2", message2, signature2),
    ]

    print("ECDSA Signature Verification Results:\n")

    for description, msg, sig in tests:
        result = verify_signature(public_key, msg, sig)
        print(f"{description}: {'VALID' if result else 'INVALID'}")


if __name__ == "__main__":
    main()
