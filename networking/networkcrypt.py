from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class NetworkEncryption:
    def __init__(self):
        self.public_key = self.load_pubkey()

    @staticmethod
    def gen_rsakeys():
        '''Generates private and public RSA keys that are saved in folder /keys'''
        
        # Generate and save RSA private_key to keys/private_key.pem
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                        format=serialization.PrivateFormat.PKCS8,
                                        encryption_algorithm=serialization.BestAvailableEncryption(b'8hPr2q2ntPMXQ2dPAfqJxGyyrH2U*XI(hIEnaHNHC&vTwWJNVX9KqYRwrem2WmPZ'))
        pem.splitlines()[0]

        with open("../keys/private_key.pem", 'wb') as pem_out:
            pem_out.write(pem)
        
        # Generate and save RSA public_key to keys/public_key.pem
        public_key = private_key.public_key()
        pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                      format=serialization.PublicFormat.SubjectPublicKeyInfo)
        pem.splitlines()[0]
        with open("../keys/public_key.pem", 'wb') as pem_out:
            pem_out.write(pem)

    def load_pubkey(self):
        '''Load public_key from file saved in folder /keys'''
        with open("keys/public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
            return public_key

    def encrypt_data(self, data) -> bytes:
        """Uses RSA public key to encrypt data for the server to decrypt
        @Parameters
            data : bytes
                The data to encrypt, this needs to either be pickled or if its a string, it needs to be converted to bytes.
        """

        ciphertext = self.public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return ciphertext

if __name__ == "__main__":
    NetworkEncryption.gen_rsakeys()