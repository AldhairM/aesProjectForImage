from Crypto.Cipher import AES
from Crypto import Random
import binascii
import base64



def saturar(inp, blocksize=128):
    tam_sat = blocksize - (len(inp) % blocksize)  
    relleno = b'a'*tam_sat
    return inp + relleno

def remove_space_padding(strl, blocksize=128):
    tam_sat = 0 
    for char in strl[::-1]: 
        if char == 'a':
            tam_sat += 1
        else:
            break

    stlr = strl[:-tam_sat]
   
    return strl

def encrypt(plaintext, key, mode="ECB"):
    if mode == "OCB" :
        des = AES.new(key, AES.MODE_OCB)
        cipher = des.encrypt(plaintext)
        non = des.nonce
        return  cipher, non
    if mode == "CTR" :
        des = AES.new(key, AES.MODE_CTR)
        cipher = des.encrypt(plaintext)
        non = des.nonce
        return  cipher, non
    if mode == "OFB" :
        des = AES.new(key, AES.MODE_OFB)
        cipher = des.encrypt(plaintext)
        iv = des.iv
        return  cipher, iv
    if mode == "GCM" :
        des = AES.new(key, AES.MODE_GCM)
        cipher = des.encrypt(plaintext)
        non = des.nonce
        return  cipher, non
    else:
        des = AES.new(key, AES.MODE_ECB)
        return des.encrypt(plaintext)
                           
def decrypt(ciphertext, key, mode="ECB", nonce=None):
    if mode == "OCB":
        des = AES.new(key, AES.MODE_OCB, nonce=nonce)
        return des.decrypt(ciphertext)
    if mode == "CTR":
        des = AES.new(key, AES.MODE_CTR, nonce=nonce)
        return des.decrypt(ciphertext)
    if mode == "OFB":
        des = AES.new(key, AES.MODE_OFB, iv=nonce)
        return des.decrypt(ciphertext)
    if mode == "GCM":
        des = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return des.decrypt(ciphertext)
    else:
        des = AES.new(key, AES.MODE_ECB)
        return des.decrypt(ciphertext)
 

                           
if __name__ == "__main__":

    #key is 128 bits = 16 bytes
    key = Random.new().read(16)
    print("Key: {}".format(key))
    test = bytearray(128)
    plaintext = base64.b64encode(test)
    appended = saturar(plaintext)
    ciphertext= encrypt(appended,key)
    decrypted = decrypt(ciphertext,key)
    print("desencriptado {}".format(getsizeof(decrypted)))
    satured= remove_space_padding(decrypted)
    plaintextout = base64.b64decode(satured)
    print(plaintextout)