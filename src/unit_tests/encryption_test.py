def test_encrypt_data(encryption):
    encryption.encrypt_data(b"hello")


def test_decrypt_data(encryption):
    encryption.decrypt_data(b"hello")
