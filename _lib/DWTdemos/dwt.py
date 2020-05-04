import numpy as np
import pywt 
import cv2 
import imageio
from sys import getsizeof



def ProcesoDWT(name):
    coeffs = pywt.wavedecn(name, wavelet='db2',level = 1)
    arr, coeff_slices, coeff_shapes = pywt.ravel_coeffs(coeffs)
    coeffs_from_arr = pywt.unravel_coeffs(arr, coeff_slices, coeff_shapes, output_format='wavedecn')
    return coeffs_from_arr

def separar_Coef(coeffs_from_arr):
    a =coeffs_from_arr[0]
    h =coeffs_from_arr[1]["ad"]
    v =coeffs_from_arr[1]["da"]
    d =coeffs_from_arr[1]["dd"]
    return a, h, v, d

def clear_Txt():
    names = ["a","h","v","d"]
    for n in names:
        with open("{}.txt".format(n),"r") as start, open("{}d.txt".format(n),"w") as out:
            mutable = start.read()
            size=getsizeof(mutable)
            for char in reversed(range(size)):
                try:
                    if mutable[char] == "\n":
                        out.write(mutable[:char])
                        break
                except IndexError:
                    pass

def Save_txt(coeffs_from_arr):
    a, h, v, d = separar_Coef(coeffs_from_arr)
    array = [a,h,v,d]
    b = ["a","h", "v", "d"]
    for n in range(len(array)):
        np.savetxt('{}.txt'.format(b[n]), array[n])

def load_txt():
    a = np.genfromtxt('ad.txt')
    h = np.genfromtxt('hd.txt')
    v = np.genfromtxt('vd.txt')
    d = np.genfromtxt('dd.txt')
    return a, h, v, d

def unir_Coef():
    a,h,v,d = load_txt()
    s = dict({"ad": h, "da": v, "dd": d}) 
    coeffs_from_arr = [a, s]
    return coeffs_from_arr

def ReconstructDWT():
    clear_Txt()
    coeffs_from_arr = unir_Coef()
    name_recon = pywt.waverecn(coeffs_from_arr, wavelet='db2')
    return name_recon

if __name__ == "__main__":
    data = "lena"
    name = "{}.png".format(data)
    name = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
    coeffs_from_arr = ProcesoDWT(name)
    Save_txt(coeffs_from_arr)
    name_recon = ReconstructDWT()
    imageio.imwrite('{}_des.png'.format(data), name_recon)
    data = "{} procesada".format(data)
    print (data)