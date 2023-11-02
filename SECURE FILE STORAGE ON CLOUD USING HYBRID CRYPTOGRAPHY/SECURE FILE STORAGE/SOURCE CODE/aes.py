from Crypto.Cipher import AES
def encryptData(data):
    key = b'venuuyd'
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    print(ciphertext)

def decryptData(data):
    print('')



result = encryptData('hiiii how are you')
print(result)
result2 = decryptData(result)
print(result2)