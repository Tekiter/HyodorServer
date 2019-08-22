from cryptography.fernet import Fernet

key = b'qR4acRqJQwh_9VOqPFXG1Wl4kxNzBzgehkHyyDgQDoA='

engine = Fernet(key)


def encrypt(content):
    return engine.encrypt(content).decode()

def decrypt(encrypted):
    return engine.decrypt(encrypted)