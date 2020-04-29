#!/usr/bin/env python
# coding: utf-8

# In[1]:


import aes
import dwt4 as dwt
from Huff import HuffmanCoding
from Crypto import Random
import cv2
import os
import imageio
import binascii
from base64 import b64decode, b64encode
from sys import getsizeof
import time

# In[3]:
start = time.time()

name = "lena.png"
data = cv2.imread(name, cv2.IMREAD_GRAYSCALE)


# In[4]:


coeffs_from_arr = dwt.ProcesoDWT(data)
dwt.Save_txt(coeffs_from_arr)


# In[5]:


names = ["a", "h", "v", "d"]
key = Random.new().read(16)


# In[6]:


h = HuffmanCoding()
for cr in range(len(names)):
    path = "{}.txt".format(names[cr])
    h.compress(path)


# In[7]:


for cr in range(len(names)):
    n=names[cr]
    with open("{}_c.bin".format(n),"rb") as file, open("{}_cl.bin".format(n),"wb") as out:
        plaintext = b64encode(file.read())
        appended = aes.saturar(plaintext)
        ciphertext= aes.encrypt(appended,key)
        print(getsizeof(ciphertext))
        decrypted = aes.decrypt(ciphertext,key)
        print("desencriptado {}".format(getsizeof(decrypted)))
        satured= aes.remove_space_padding(decrypted)
        plaintextout = b64decode(satured)
        print(getsizeof(plaintextout))
        out.write(plaintextout)
        file.close()
        out.close()


# In[8]:


h = HuffmanCoding()
for cr in range(len(names)):
    path = "{}_cl.bin".format(names[cr])
    h.decompress(path)


# In[9]:


name_recon = dwt.ReconstructDWT()


# In[10]:


imageio.imwrite('lena_sd.png', name_recon)

end = time.time()
timed= start - end
print(timed)