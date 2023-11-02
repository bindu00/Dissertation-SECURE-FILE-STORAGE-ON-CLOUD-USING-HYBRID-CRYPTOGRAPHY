from Crypto.Cipher import DES3
from Crypto import Random
import os
class MyTrippleDesk:
    def encrypt_trippleDesk(self,plaintext):
        key = os.urandom(16)
        iv = Random.new().read(DES3.block_size)
        cipher_encrypt = DES3.new(key, DES3.MODE_OFB, iv)
        return iv,key,cipher_encrypt.encrypt(plaintext)
    def decrypt_trippleDesk(self,iv, key, encrypted_text):
        cipher_decrypt = DES3.new(key, DES3.MODE_OFB, iv)
        return cipher_decrypt.decrypt(encrypted_text)

# plaintext = b'hiiii how are you'
# iv,key, cipher_encrypt = encrypt_trippleDesk(plaintext)
# print(key)
# print(cipher_encrypt)
# data =decrypt_trippleDesk(iv, key, cipher_encrypt)
# print(data)