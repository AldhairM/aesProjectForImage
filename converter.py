import numpy as np
import imageio


def convertImage(name, image, shape):
    with open(name,"rb") as file:
        text=file.read()
        
        width=shape
        if shape%2 !=0:
            width=shape+1
        
        state=True
        while(state):
            if len(text)%width==0:
                state=False
            else:
                width+=1
    
        array=[]
        matrix=[]
        counter=0
        for num in range(len(text)):
            try:
                if counter == width:
                    matrix.append(array)
                    array=[]
                    counter = 1
                    array.append(text[num-1])
                else:
                    array.append(text[num-1])
                    counter += 1 
            except:
                pass
        imageio.imsave(f"{image}.png",np.array(matrix))