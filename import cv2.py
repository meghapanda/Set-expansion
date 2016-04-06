import numpy as np
from skimage.filters import threshold_otsu, rank
import math
li=[0.75,0.75,0.70,0.65,0.6]
#a=np.array(li,np.float8)
a=np.array(li)
print(a)#


#  z = np.array([(12),(13),(56),(2020),(145)],np.uint8)
T = threshold_otsu(a)
T=round(T,2)
print(T)


K=sum(a>=T)
print(K)