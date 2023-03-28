import os

from google.cloud import kms

DATASET_ENCRYPTION = os.environ.get("DATASET_ENCRYPTION", "true").lower() == "true"
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")

if DATASET_ENCRYPTION:
    if not GOOGLE_CLOUD_PROJECT:
        raise Exception("You need to set GOOGLE_CLOUD_PROJECT")
client = kms.KeyManagementServiceClient()
key_name = client.crypto_key_path(
    GOOGLE_CLOUD_PROJECT, "global", "sds_keyring", "unit_data_key"
)


def encrypt_data(plaintext_data: bytes):
    request = {"name": key_name, "plaintext": plaintext_data}
    encrypted_data = client.encrypt(request, timeout=2)
    return encrypted_data.ciphertext


def decrypt_data(ciphertext: bytes):
    request = {"name": key_name, "ciphertext": ciphertext}
    decrypt_response = client.decrypt(request, timeout=2)
    return decrypt_response.plaintext
