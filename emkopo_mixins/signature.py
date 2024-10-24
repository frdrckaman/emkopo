import base64
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from xml.etree.ElementTree import ElementTree, fromstring

from django.conf import settings


def sign_data(private_key, data):
    """
    Sign the data using the private key.
    """
    signature = private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

def load_private_key(file_path, password=None):
    """
    Load the private key from the PEM file.
    If the key is encrypted, provide the password.
    """
    with open(file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=password.encode() if password else None,
            backend=default_backend()
        )
    return private_key


def load_public_key_from_crt(crt_file_path):
    """
    Load the public key from a .crt file.
    """
    with open(crt_file_path, 'rb') as crt_file:
        crt_data = crt_file.read()

    # Load the X.509 certificate
    cert = load_pem_x509_certificate(crt_data, default_backend())

    # Extract the public key from the certificate
    public_key = cert.public_key()
    return public_key

def verify_xml_signature(xml_payload):
    """
    Verifies the signature of an XML payload using the extracted public key.
    """

    public_key = load_public_key_from_crt(settings.ESS_PUBLIC_KEY)
    # Parse the XML to extract the signature and the signed data
    tree = ElementTree(fromstring(xml_payload))
    root = tree.getroot()

    # Extract the Signature (Assuming it's in <Signature>...</Signature>)
    signature_element = root.find(".//Signature")
    if signature_element is None:
        raise ValueError("No Signature element found in XML")

    signature_b64 = signature_element.text.strip()

    # Remove signature element from the tree
    signature_element.clear()  # Remove signature from XML tree

    # Convert the XML to a string (canonicalization might be needed here)
    unsigned_xml_string = ElementTree.tostring(root, encoding="utf-8").decode("utf-8")

    # Convert the XML string to bytes for verification
    unsigned_xml_bytes = unsigned_xml_string.encode('utf-8')

    # Decode the signature from base64
    signature_bytes = base64.b64decode(signature_b64)

    # Verify the signature using the public key
    try:
        public_key.verify(
            signature_bytes,
            unsigned_xml_bytes,
            padding.PKCS1v15(),  # Padding used in the signature (RSA)
            hashes.SHA256()  # Hash algorithm used to sign the data
        )
        print("Signature is valid")
        return True
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return False