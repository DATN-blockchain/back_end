import base64

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def hash_verify_code(verify_code: str):
    return pwd_context.hash(verify_code)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def verify_code(code: str, verify_code: str):
    return pwd_context.verify(code, verify_code)


def base64_encode(data):
    if isinstance(data, dict):
        data = str(data)

    if not isinstance(data, bytes):
        data = data.encode('utf-8')
    encoded_data = base64.b64encode(data)
    return encoded_data.decode('utf-8')


def base64_decode(encoded_data):
    encoded_bytes = encoded_data.encode('utf-8')
    decoded_data = base64.b64decode(encoded_bytes)

    return decoded_data.decode('utf-8')


if __name__ == '__main__':
    data = dict(a=1,b=2)
    a=base64_encode(data)
    print(len(a))
    print(hash_password("123123"))
