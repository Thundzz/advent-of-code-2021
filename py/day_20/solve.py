from scipy import ndimage
from  functools import lru_cache
import numpy as np

def to_int(c):
    return 1 if c == "#" else 0

def parse_input(filename):
    with open(filename) as file:
        content = file.read()
    algo, img = content.split("\n\n")
    img = np.matrix([ list(map(to_int, l)) for l in img.strip().split("\n")  ])
    return algo.strip(), img

@lru_cache
def mapping_func(algorithm):
    def func(idx):
        return to_int(algorithm[int(idx)])
    return np.vectorize(func)

def convolve(mat, kernel, background):
    n, m = mat.shape
    n_k, m_k = kernel.shape
    new_img = np.zeros_like(mat)
    for i in range(0, n):
        for j in range(0, m):
            res = 0
            for ii in [-1, 0, 1]:
                for jj in [-1, 0,  1]:
                    if 1 <= i + ii < n and 1<= j +jj < m:
                        res += mat[i + ii, j  + jj] * kernel[ii+1,jj+1]
                    else:
                        res += background * kernel[ii+1,jj+1]
            new_img[i, j] = res
    return new_img

def enhance(img, algorithm, background):
    vmapping = mapping_func(algorithm)
    kernel = np.matrix([
        [256,  128,   64],
        [ 32,   16,    8],
        [  4,    2,    1]
    ])
    n, m = img.shape
    if background == 0:
        mat = np.zeros((n+2, m+2), dtype=int)
    else:
        mat = np.ones((n+2, m+2), dtype=int)
    mat[1:n+1, 1:m+1] = img
    conv = convolve(mat, kernel, background)
    res = vmapping(conv)
    return res, vmapping(511 if background == 1 else 0)

def plot(res):
    import matplotlib.pyplot as plt
    plt.imshow(res)
    plt.show()


def main():
    algo, img = parse_input("input.txt")
    background = 0
    for i in range(50):
        img, background = enhance(img, algo, background)
    print(len(np.argwhere(img == 1)))

if __name__ == '__main__':
    main()



