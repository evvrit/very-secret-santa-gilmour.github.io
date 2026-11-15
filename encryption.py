import base64
import hashlib
import json
import secrets

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from pick import pick

# no 0/1/I/L/O, so codes are easy to read and type
ALPHABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
CODE_LEN = 16
PAYLOAD_PAD = 32  # pad so blob length doesn't hint "Ike" vs "Laura"

def new_code():
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LEN))

def normalize(code):
    return code.upper().replace("-", "").replace(" ", "")

def key_from_code(code):
    return hashlib.sha256(normalize(code).encode()).digest()

def encrypt_pair(code, gifter, recipient):
    payload = f"{gifter}\n{recipient}".encode()
    assert len(payload) <= PAYLOAD_PAD, f"names too long to pad: {gifter}, {recipient}"

    iv = secrets.token_bytes(12)
    padded = payload.ljust(PAYLOAD_PAD, b"\0")
    ciphertext = AESGCM(key_from_code(code)).encrypt(iv, padded, None)
    return base64.b64encode(iv + ciphertext).decode()

def pretty(code):
    return "-".join(code[i:i + 4] for i in range(0, CODE_LEN, 4))

def encrypt_all(pairs):
    codes, blobs = {}, []

    for gifter, recipient in pairs:
        code = new_code()
        codes[gifter] = pretty(code)
        blobs.append(encrypt_pair(code, gifter, recipient))

    # blob order mustn't match gifter order
    secrets.SystemRandom().shuffle(blobs)

    return codes, blobs

if __name__ == "__main__":
    codes, blobs = encrypt_all(pick())

    # hand these out privately, one per person
    with open("codes.txt", "w") as file:
        for gifter, code in codes.items():
            file.write(f"{gifter}: {code}\n")

    # safe to publish: paste into BLOBS in index.html
    with open("blobs.json", "w") as file:
        json.dump(blobs, file, indent=2)

    print("wrote codes.txt and blobs.json")
