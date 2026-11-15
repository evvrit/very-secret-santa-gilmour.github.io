from cryptography.fernet import Fernet
from pick import pick

def get_key():
    with open("fernet.key", "rb") as file:
        return file.read().strip()

fernet_key = get_key()

def encrypt(name):
    f = Fernet(fernet_key)
    message = name.encode()
    enc_message = f.encrypt(message)
    return enc_message.decode()

def encrypt_all(pairs):
    encrypted_pairs = []

    for pair in pairs:
        gifter = pair[0]
        name_to_encrypt = pair[1]

        encrypted_name = encrypt(name_to_encrypt)

        encrypted_pair = (gifter, encrypted_name)
        encrypted_pairs.append(encrypted_pair)

    return encrypted_pairs

def decrypt(enc_message):
    f = Fernet(fernet_key)
    dec_message = f.decrypt(enc_message)
    return dec_message.decode()

pairs = pick()
encrypted_pairs = encrypt_all(pairs)
print(encrypted_pairs)

for enc_pair in encrypted_pairs:
    gifter = enc_pair[0]
    enc_recipient = enc_pair[1]
    print(gifter, enc_recipient)
    dec_recipient = decrypt(enc_recipient)
    print(gifter, dec_recipient)
