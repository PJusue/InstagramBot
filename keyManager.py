from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537,
                                           key_size=2048,
                                           backend=default_backend()
                                           )
    public_key = private_key.public_key()
    return public_key, private_key


def storing_private_key(private_key):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
    with open('pvkey.pem', 'wb') as f:
        f.write(pem)


def storing_public_key(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('pbkey.pem', 'wb') as f:
        f.write(pem)

def open_public_Key():
    with open("pbkey.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )
    return public_key

def open_private_key():
    with open("pvkey.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )
    return private_key

def main():
    public_key, private_key = generate_keys()
    storing_private_key(private_key)
    storing_public_key(public_key)


if __name__ == "__main__":
    main()
