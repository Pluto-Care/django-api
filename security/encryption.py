import json
from Crypto.Cipher import AES


def encrypt(key_path, obj):
    # Get the key
    with open(key_path, 'rb') as f:
        key = f.read()

    cipher = AES.new(key, AES.MODE_EAX)

    # Encrypt
    ciphertext, tag = cipher.encrypt_and_digest(str.encode(json.dumps(obj)))
    encrypted = [x for x in (cipher.nonce, tag, ciphertext)]
    return b''.join(encrypted)


def decrypt(key_path, obj):
    # Get the key
    with open(key_path, 'rb') as f:
        key = f.read()
    nonce, tag, ciphertext = obj[:16], obj[16:32], obj[32:]
    try:
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return json.loads(data)
    except ValueError:
        return None
