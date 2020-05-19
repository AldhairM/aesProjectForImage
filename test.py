

img=[["barbara"],["color"],["eye"],["lena"],["lenaV2"],["logo"],["Mandrill"],["peppers"],["pinguin"],["scale"]]


# # PSNR y MSE
# https://www.geeksforgeeks.org/python-peak-signal-to-noise-ratio-psnr/

from math import log10, sqrt 
import cv2
import numpy as np 
import skimage    
import imageio


def PSNR(original, compressed): 
    mse = np.mean((original - compressed) ** 2) 
    if(mse == 0):  # MSE is zero means no noise is present in the signal . 
                  # Therefore PSNR have no importance. 
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse)) 
    return psnr, mse


def calculate_psnr(img1, img2, max_value=255):
    """"Calculating peak signal-to-noise ratio (PSNR) between two images."""
    mse = np.mean((np.array(img1, dtype=np.float32) - np.array(img2, dtype=np.float32)) ** 2)
    if mse == 0:
        return 100
    psnr = 20 * np.log10(max_value / (np.sqrt(mse)))
    return psnr, mse


def npcr(inpt1,inpt2):
    Rows1=len(inpt1)
    Cols1=len(inpt1[0])
    Rows2=len(inpt2)
    Cols2=len(inpt2[0])
    if Rows1 == Rows2 and Cols1 == Cols2:
        # Calculo del NPCR
        D1=np.zeros(Rows1*Cols1).astype(float)
        D2=np.reshape(D1, (Rows1, Cols1))
        counter=0
        for row in range(Rows1):
            for col in range(Cols1):
                if inpt1.all == inpt2.all:
                    D2[row][col]=0
                else:
                    D2[row][col]=1
                    counter=counter+1
        npcr=float(100*counter)/float(Rows1*Cols1)
        return npcr
    else:
        n="Las dimensiones de las entradas a la funcion npcr no concuerdan"
        return n


# # UACI

def uaci(image1,image2): 
    pixel1=image1
    pixel2=image2
    sizeImage=image1.shape
    value=0.0
    for y in range(0,sizeImage[1]):
        for x in range(0,sizeImage[0]):
            value=(abs(pixel1[x,y][0]-pixel2[x,y][0])/255)+value

    value=(value/(sizeImage[0]*sizeImage[1]))*100
    return value

def uacil(inpt1,inpt2):
    Rows1=len(inpt1)
    Cols1=len(inpt1[0])
    Rows2=len(inpt2)
    Cols2=len(inpt2[0])
    if Rows1 == Rows2 and Cols1 == Cols2:
        # Calculo del NPCR
        D1=np.zeros(Rows1*Cols1).astype(float)
        D2=np.reshape(D1, (Rows1, Cols1))
        meanerror=0.0
        error=0.0
        for row in range(Rows1):
            for col in range(Cols1):
                error=abs(float(inpt1[row][col])-float(inpt2[row][col]))
                meanerror=float(meanerror+error)
        uaciResult=float(100*meanerror)/float(255*Rows1*Cols1)
        return uaciResult
    else:
        return "Las dimensiones de las entradas a la funcion npcr no concuerdan"

# ## Entropia

def entropyf(init):
    marg = np.histogramdd(np.ravel(init), bins = 256)[0]/init.size
    marg = list(filter(lambda p: p > 0, np.ravel(marg)))
    entropy = -np.sum(np.multiply(marg, np.log2(marg)))
    return entropy

def entropySKI(init):
    return skimage.measure.shannon_entropy(init)



def testing(name,dir=""):
    data=[["PSNR"],["NPCR"],["UACI"],["Entropy"]]
    files=[f"{name}_init.png",f"{name}_mid.png",f"{name}_out.png"]
    
    init=cv2.imread(files[0])
    mid=cv2.imread(files[1])
    out=cv2.imread(files[2])
    
    initG=cv2.imread(files[0], cv2.IMREAD_GRAYSCALE)
    midG=cv2.imread(files[1], cv2.IMREAD_GRAYSCALE)
    outG=cv2.imread(files[2], cv2.IMREAD_GRAYSCALE)
    
    try:
        p1m=PSNR(initG,midG)
        p1o=PSNR(initG,outG)
        p2m=calculate_psnr(initG,midG)
        p2o=calculate_psnr(initG,outG)
    except:
        p1o,p2o="fail","fail"
        p1m,p2m="fail","fail"
    try:
        n1m=npcr(initG,midG)
        n1o=npcr(initG,outG)
    except:
        n1m="fail"
        n1o="fail"
    try:
        u1m=uaci(init, mid)
        u1o=uaci(init, out)
        u2m=uacil(initG, midG)
        u2o=uacil(initG, outG)
    except:
        u1m, u2m="fail", "fail"
        u1o, u2o="fail", "fail"
        
    try:
        e1i=entropySKI(init)
        e2i=entropyf(init)
    except:
        e1i,e2i="fail","fail"

    try:
        e1m=entropySKI(mid)
        e2m=entropyf(mid)
    except:
        e1m,e2m="fail","fail"
    
    try:
        e1o=entropySKI(out)
        e2o=entropyf(out)
    except:
        e1o,e2o="fail","fail"
    
    data[0].append([p1m,p2m,p1o,p2o])
    data[1].append([n1m,n1o])
    data[2].append([u1m,u2m,u1o,u2o])
    data[3].append([e1i,e2i,e1m,e2m,e1o,e2o])
    return data




