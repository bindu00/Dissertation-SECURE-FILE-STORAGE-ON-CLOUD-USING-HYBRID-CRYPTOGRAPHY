from Crypto.Cipher import AES
import binascii, os
class MyAES:
    def encrypt_AES_GCM(self,msg):
        secretKey = os.urandom(32)
        aesCipher = AES.new(secretKey, AES.MODE_GCM)
        ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
        return secretKey,(ciphertext, aesCipher.nonce, authTag)

    def decrypt_AES_GCM(self,encryptedMsg, secretKey):
        (ciphertext, nonce, authTag) = encryptedMsg
        aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
        plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
        return plaintext

# myaes = MyAES()
# msg = b'hiii how are youf ffafaffafdasfdasfdasfasdfasfafadsfedadwe'
# key, encryptedMsg = myaes.encrypt_AES_GCM(msg)
# decryptedMsg = myaes.decrypt_AES_GCM(encryptedMsg, key)
# print(encryptedMsg)
# print(decryptedMsg)
# print(key)
# secretKey = binascii.hexlify(encryptedMsg[0])
# print(secretKey)
# secretKey = binascii.unhexlify(secretKey)
# print(secretKey)
