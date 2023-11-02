from Crypto.Cipher import Blowfish
from Crypto import Random
import os
class MyBlowFish:
    def encrypt_blowFish(self,plaintext):
        key = os.urandom(16)
        iv = Random.new().read(Blowfish.block_size)
        cipher_encrypt = Blowfish.new(key,Blowfish.MODE_OFB,iv)
        return iv,key,cipher_encrypt.encrypt(plaintext)
    def decrypt_blowfish(self,iv, key, encrypted_text):
        cipher_decrypt = Blowfish.new(key,Blowfish.MODE_OFB,iv)
        return cipher_decrypt.decrypt(encrypted_text)

# plaintext = b'hiiii how are you'
# iv, key, cipher_encrypt = encrypt_blowFish(plaintext)
# print(iv)
# print(key)
# print(cipher_encrypt)
# data =decrypt_blowfish(iv, key, cipher_encrypt)
# print(data)