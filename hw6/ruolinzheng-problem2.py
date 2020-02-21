#!/usr/bin/env python3
from urllib.parse import quote
import urllib.request
import base64
import ssl
import time
import re

################################################################################
# 
# This starter file for UChicago CMSC 23200 / 33250 is for Python 3
#
################################################################################

################################################################################
# 
# make_query(username, password)
# -- username is a string that represents a potential username on the server
# -- password is a string that represents that user's potential password
#
################################################################################

def make_query(username, password):
    DEBUG = False; # Replace with "True" to print extra debugging information
    username = username.lower()
    if DEBUG:
        print("Querying the server")
        print("(username:", username, ")")
        print("(password:", password, ")")
    url = "https://uchicago.computer/" + urllib.parse.quote(username) + "/" + urllib.parse.quote(password) + "/"
    if DEBUG:
        print("(Querying:", url, ")")
    start = time.time()
    with urllib.request.urlopen(url) as response:
        ret = response.read().decode('utf-8')
    end = time.time()
    return end - start, ret

def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    # process the files to match usernames with Hashcat-cracket passwords
    with open('ruolinzheng-problem1.potfile', 'rt') as f:
        hashes = f.readlines()
    with open('shadow.txt', 'rt') as f:
        shadow = f.readlines()
    hash_user_dict = {} # {hash: username}
    for line in shadow:
        parts = re.split(r':', line)
        user, pwhash = parts[0], parts[1]
        hash_user_dict[pwhash] = user
    hash_pw_dict = {} # {hash: password}
    for line in hashes:
        line = line.strip()
        parts = re.split(r':', line)
        pwhash, pw = parts[0], parts[1]
        hash_pw_dict[pwhash] = pw
    user_pw_dict = {}
    for pwhash in hash_pw_dict:
        user = hash_user_dict[pwhash]
        user_pw_dict[user] = hash_pw_dict[pwhash]
    with open('ruolinzheng-problem1.txt', 'wt') as f:    
        for user in user_pw_dict:
            f.write(user + '\t' + user_pw_dict[user] + '\n')

    # problem 2
    has_accounts = []
    for user in user_pw_dict:
        pw = user_pw_dict[user]
        t, resp = make_query(user, pw)
        print(user, pw, t, resp)
        if t > 1:
            has_accounts.append(user)

    print('\n\nThere are {} out of {} users that have accounts'.format(len(has_accounts), len(user_pw_dict)))
    with open('ruolinzheng-problem2.txt', 'wt') as f:
        for user in has_accounts:
            f.write(user + '\n')

if __name__ == '__main__':
    main()