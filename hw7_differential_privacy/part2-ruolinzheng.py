#!/usr/bin/env python3

import numpy as np
import struct

def float_to_binary(num):
    return ''.join(bin(c).replace('0b', '').rjust(8, '0') for c in struct.pack('!d', num))

def binary_to_float(b):
    bf = int(b, 2).to_bytes(8,'big')  
    return struct.unpack('>d', bf)[0]

def my_laplace(scale=1):
    u = np.random.uniform()
    b = np.random.randint(2)
    l = (2*b-1)*np.log(u)
    return l*scale

def is_in_U(x):
    a = x / (2 ** -53)
    b = x // (2 ** -53)
    return a == b

def is_scaled_laplace_img(y, scale):
    if y > 0:
        y = -y
    x = np.exp(y / scale)
    x2 = np.exp(np.log(x))
    if is_in_U(x) and scale * np.log(x2) == y and is_in_U(x2):
        return True
    else:
        return False

def main():
    scale = 1
    tp = 0 # true positive
    fp = 0 # false positive
    for _ in range(1000):
        y = my_laplace(scale)
        if is_scaled_laplace_img(y, scale):
            tp += 1
    for _ in range(1000):
        y2 = 1. + my_laplace(scale)
        if is_scaled_laplace_img(y2, scale):
            fp += 1
    print('True positives from my_laplace(1) is ' + str(tp))
    print('False positives from 1. + my_laplace(1) is ' + str(fp))
    print('TP and FP differ by ' + str(tp - fp))

if __name__ == '__main__':
    main()