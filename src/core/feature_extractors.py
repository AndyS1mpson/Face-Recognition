import math

import numpy as np
from scipy.fftpack import dct

from .dist import dist


def scale(image, scale = 2):
    '''Извлечение признаков методом Scale'''
    h = image.shape[0]
    w = image.shape[1]
    m, n = h // scale, w // scale
    X = image.copy().astype(np.int32)
    image_sc = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            image_sc[i, j] = np.sum(X[i*scale:min((i+1)*scale,h),j*scale:min((j+1)*scale,w)])
    return image_sc, np.asarray(image_sc).reshape(-1)


def _spec_zigzag(C, P):
    return np.array([C[y+1-k,k] for y in range(P) for k in range(y, 0, -1)])


def dft(img, P=20):
    '''Извлечение признаков методом DFT (Двумерное дискретное преобразование Фурье)'''
    C = np.abs(np.fft.fft2(img)[0:P, 0:P])
    return C, _spec_zigzag(C, P)


def dct(img, P=20):
    '''Извлечение признаков методом DCT (Двумерное дискретное косинус-преобразование)'''
    M, N = img.shape
    X = img.copy().astype(np.int32)
    t = lambda S, i, j: math.sqrt(2/S)*math.cos(math.pi*(2*j+1)*i/(2*S))
    T_P_M = np.array([[t(M, p, m) if p != 0 else 1/math.sqrt(M) for m in range(M)] for p in range(P)])
    T_N_P = np.array([[t(N, p, n)if p != 0 else 1/math.sqrt(N) for p in range(P)] for n in range(N)])
    C = np.dot(np.dot(T_P_M, X), T_N_P)
    return C, _spec_zigzag(C, P)


def hist(img, BIN=16):
    '''Извлечение признаков методом Hist (Гистограмма яркости)'''
    # return np.histogram(img, bins=BIN, normed=True)
    M, N = img.shape
    top_hist = np.array([
        np.sum(
            np.array(img[:M//2,:] >= b*(256//BIN)) &
            np.array(img[:M//2,:] <= (b+1)*(256//BIN)-1)
        )
        for b in range(BIN)
    ])
    bottom_hist = np.array([
        np.sum(
            np.array(img[M//2:,:] >= b*(256//BIN)) & 
            np.array(img[M//2:,:] <= (b+1)*(256//BIN)-1)
        ) 
        for b in range(BIN)
    ])
    h = np.concatenate((top_hist, bottom_hist)) / (M*N)
    return (np.array(range(2*BIN)), h), h
    

def grad(img, W=16):
    '''Извлечение признаков методом Gradient'''
    M, _ = img.shape
    X = img.copy().astype(np.int32)
    grads = []
    for x in range(W,M-W):
        top = X[x-W:x,:]
        bottom = np.flip(X[x:x+W,:], axis=0)
        grads.append(dist(top, bottom))
    grads = np.array(grads)
    return (np.array(range(len(grads))), grads), grads


HANDLER = {
    scale.__name__: scale,
    hist.__name__: hist,
    grad.__name__: grad,
    dft.__name__: dft,
    dct.__name__: dct
}
