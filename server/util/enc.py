from cryptography.fernet import Fernet

key = b'qR4acRqJQwh_9VOqPFXG1Wl4kxNzBzgehkHyyDgQDoA='

engine = Fernet(key)


def encrypt(content: str):
    return engine.encrypt(content.encode()).decode()

def decrypt(encrypted) -> str:
    return engine.decrypt(encrypted.encode()).decode()