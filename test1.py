import numpy as np

a=np.array([["1"]*2]*3)
b=np.zeros((5,7),dtype=str)
print(b)
sy=b.shape[0]//2-a.shape[0]//2
sx=b.shape[1]//2-a.shape[1]//2
ey=b.shape[0]//2+a.shape[0]//2+a.shape[0]%2
ex=b.shape[1]//2+a.shape[1]//2+a.shape[1]%2
b[sy:ey,sx:ex]=a
return b
print(b)