#!/usr/bin/env python3

import urllib.request
import base64
import math
import sys
import re
from decimal import *
from hashlib import sha256
from pymd5 import md5, padding

################################################################################
# 
# This starter file for UChicago CMSC 23200 / 33250 is for Python3
#
################################################################################

################################################################################
# 
# make_query(task, cnet_id, query)
# -- task should be one of 'one','two','three','four','five'
# -- cnet_id should always be your own cnet_id
# -- query can be any string of bytes, including non-printable
#
################################################################################

def make_query(task, cnet_id, query):
    DEBUG = False; # Replace with "True" to print extra debugging information
    task = task.lower()
    cnet_id = cnet_id.lower()
    if DEBUG: 
        print("Querying the server")
        print("(Task:", task, ")")
        print("(CNET ID:", cnet_id, ")")
        print("(Query:", query, ")")
    if (type(query) is bytearray) or (type(query) is bytes):
        url = "http://securityclass.cs.uchicago.edu/" + urllib.parse.quote_plus(task) + "/" + urllib.parse.quote_plus(cnet_id) + "/" + urllib.parse.quote_plus(base64.urlsafe_b64encode(query)) + "/"
    else:
        url = "http://securityclass.cs.uchicago.edu/" + urllib.parse.quote_plus(task) + "/" + urllib.parse.quote_plus(cnet_id) + "/" + urllib.parse.quote_plus(base64.urlsafe_b64encode(query.encode('utf-8'))) + "/"
    if DEBUG:
        print("(Querying:", url, ")")
    with urllib.request.urlopen(url) as response:
       answer = base64.urlsafe_b64decode(response.read())
       return answer

################################################################################
# Constants for the attacks - Don't change these!
################################################################################

e3 = 65537
k3 = 512
# Modulus N2 is 512 bits long, too short for real security
N3= 0x00dd9387a53d8eb960acc9d3bc49b859e9127ad571f95d3555dc5a30f08b832299d82ecbba38acdadfb4263947f86212f1a3894e3d308545f2618ec3a1cefc5bdf

e4 = 65537
k4 = 512
# Modulus N3 is 512 bits long, too short for real security
N4= 0x00c7d11981bf2838ed5ae602cecc4cffcf141537f9ec6e12b2fcaae43dedbf9845049066cc8720c6685d100957c07e4f5f97b2b8e66d1a3bcc32ecf1e0fee55e6f

e5 = 3
k5 = 2048
# Modulus N4 is 2048 bits long
N5 = 0x00bc9e8d81ce1de63e0ab302030e5c0595bf5d2c30fd2660ac9299431a29c4e231a675d684e35415ad87ca738509469aaa0455d62543ab9265d71767f55c7f5fdbb9e2618112212178417c21b4e8a98ab0980fd67864ed7e7e3dcefc3143d5e5d3be2bf0c36c75c977052fedbfdc1c2e448710338fad4fe0e3fa8fc2c662e3466d358df6618dc0a63f45395e5c5aa88d15a49ce2be791acbcd81e28533228918f6abb57e023145a97afea85ad238686f51409017a4d6af8687f7a9438f09a2d9d9e619abdde8e67fc95af23dc97b4a595baa26bfeaf16d31b93e3e1bae1f5813fcd9ef2c8f93df2dd4a779626d07852f120e6b84d936abb811fd4525d9a0cf6621


################################################################################
# Helper methods go below here
################################################################################

#
# modexp(base,exp,modulus) computes (base**exp) % modulus efficiently.
#
# In particular this method can handle very large values of exp, while
# the python builtin ** operator can not.
#
# Feel free to change this if you want, but you probably won't need to.
#
def modexp(base, exp, modulus):
    ret = 1
    while exp > 0:
        if exp % 2 == 1:
            ret = (ret*base) % modulus
        base = (base*base) % modulus
        exp = exp >> 1
    return ret

def cube_root_bs(num):
    """A binary search method to find the cube root of a number"""
    e = 0.000001
    start, end = 0, num
    while start < end:
        mid = Decimal(start + end) / Decimal(2)
        diff = num - mid * mid * mid
        if abs(diff) <= e:
            return mid
        elif diff > 0:
            start = mid
        else:
            end = mid

################################################################################
# PROBLEM 1 SOLUTION
################################################################################

def problem1(cnetid):
    url = b'http://www.flickur.com/?api_tag='
    resp = make_query('one', cnetid, '')
    tag = re.findall(b'api_tag=(\w+)&uname', resp)[0]
    param = b'&uname=' + cnetid.encode('utf-8') + b'&role=user'
    start = len(param) * 8
    stop = (64 + 1024) * 8 + 1 # max len of secret||param
    for i in range(start, stop, 8):
        pad = padding(i)
        padded_param = param + pad
        # round to the next multiple of 512 since secret||padded_param is a mult of 512
        counter = math.ceil(len(padded_param) * 8 / 512) * 512
        # start at secret||padded_param
        h = md5(state=bytes.fromhex(tag.decode('utf-8')), count=counter)
        h.update('&role=admin')
        forged_tag = h.hexdigest()
        padded_param += b'&role=admin'
        attack = url + forged_tag.encode('utf-8') + padded_param
        res = make_query('one', cnetid, attack)
        if b'flag' in res:
            return res

################################################################################
# PROBLEM 3 SOLUTION
################################################################################

def problem3(cnetid):
    resp = make_query('three', cnetid, '')
    ctext = int(resp.decode('utf-8'), 16)
    mult = modexp(256, e3, N3)
    attack = ctext * mult % N3
    return make_query('three', cnetid, hex(attack))


################################################################################
# PROBLEM 4 SOLUTION
################################################################################

def problem4(cnetid):
    getcontext().prec = k4
    ctext = int(make_query('four', cnetid, ''), 16)
    lo, hi = Decimal(0), Decimal(N4)
    mult = modexp(2, e4, N4)
    ctext = ctext * mult % N4
    ret = None
    while lo < hi:
        mid = (lo + hi) / Decimal(2)
        resp = make_query('four', cnetid, hex(ctext))
        if resp == b'\x00':
            hi = mid
        else:
            lo = mid
        ret = math.ceil(lo)
        if math.floor(hi) == ret:
            break
        ctext = ctext * mult % N4
    if ret is None:
        raise
    return bytes.fromhex(format(ret, 'x'))

################################################################################
# PROBLEM 5 SOLUTION
################################################################################

def problem5(cnetid):
    getcontext().prec = k5
    h = sha256()
    h.update(bytes(cnetid, 'utf-8'))
    digest = h.digest()
    pad = b'\x00\x01\xff\x00'
    start = pad + digest + b'\x00' * (256 - len(pad) - len(digest))
    signature = math.ceil(cube_root_bs(int(start.hex(), 16)))
    return make_query('five', cnetid, hex(signature))

def main():
    cnetid = 'ruolinzheng'
    if len(sys.argv) > 1:
        cnetid = sys.argv[1]
    print('Problem 1:\n', problem1(cnetid), '\n')
    print('Problem 3:\n', problem3(cnetid), '\n')
    print('Problem 4:\n', problem4(cnetid), '\n')
    print('Problem 5:\n', problem5(cnetid), '\n')

if __name__ == "__main__":
    main()
