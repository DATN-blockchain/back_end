from cryptography.fernet import Fernet


# from app.core.settings import settings


def hash_code_private_key(private_key: str):
    cipher_suite = Fernet("79bKcEhEJreCBpci75qe1iCV84QJGPSfs0I73smuzYE=")
    data = private_key.encode('utf-8')
    return cipher_suite.encrypt(data).decode('utf-8')


def decode_private_key(hash_code: str):
    cipher_suite = Fernet("79bKcEhEJreCBpci75qe1iCV84QJGPSfs0I73smuzYE=")
    return cipher_suite.decrypt(hash_code).decode('utf-8')


if __name__ == "__main__":
    encode = hash_code_private_key("0xc6bb0ae730ea89d98304bc7e7748b9d4dec9b17129e632d158c3dbdb6feb8da7")
    decode = decode_private_key(encode)
    print(encode)
    print(decode)
