#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

################################################################################
# Problem 1.1
################################################################################

def deidentify(df):
    return df.drop(columns=['Name', 'SSN'])

def pii(df):
    return df[['Name', 'DOB', 'SSN', 'Zip']]

def link_attack(deidenfied_df, pii_df):
    cols = list(set(deidentified_df.columns).intersection(set(pii_df.columns)))
    unique_did_df = deidentified_df.drop_duplicates(cols)
    unique_pii_df = pii_df.drop_duplicates(cols)
    ret = unique_did_df.merge(unique_pii_df, on=cols)
    return ret

################################################################################
# Problem 1.2
################################################################################

def is_k_anon(df, cols, k):
    count = min(df.groupby(cols).size())
    return count >= k

################################################################################
# Problem 1.3
################################################################################

def num_bachelors(df):
    return (df['Education'] == 'Bachelors').sum()

def laplace_mech(query, sensitivity, epsilon):
    return query + np.random.laplace(scale=sensitivity / epsilon)

################################################################################
# Problem 1.5
################################################################################

def plot_error():
    epsilons = [0.5, 1, 10]
    for e in epsilons:
        data = []
        for i in range(10000):
            diff = abs(laplace_mech(query, sens, e) - query)
            data.append(diff)
        plt.hist(data, bins=20, label='epsilon ' + str(e))
    plt.legend()
    plt.title('10000 datapoints, query {}, sensitivity {}'.format(query, sens))
    plt.show()

# driver/test code below here

def main():
    adult = pd.read_csv('adult.csv')
    deidentified_df = deidentify(adult)
    pii_df = pii(adult)
    print(link_attack(deidentified_df, pii_df).shape)
    assert is_k_anon(adult, ['Race', 'Sex'], 109) is True
    assert is_k_anon(adult, ['Race', 'Sex'], 110) is False
    print(num_bachelors(adult))

    query = 200
    sens = 1
    epsilons = [0.5, 1, 10]
    for e in epsilons:
        data = []
        for i in range(10000):
            data.append(laplace_mech(query, sens, e))
        plt.hist(data, bins=50, label='epsilon ' + str(e))
    plt.legend()
    plt.title('10000 datapoints, query 200, sensitivity 1')
    plt.show()

    for e in epsilons:
        data200 = []
        data201 = []
        for i in range(10000):
            data200.append(laplace_mech(200, sens, e))
            data201.append(laplace_mech(201, sens, e))
        plt.hist(data200, bins=50, label='query 200', alpha=0.8)
        plt.hist(data201, bins=50, label='query 201', alpha=0.8)
        plt.legend()
        plt.title('10000 datapoints, sensitivity 1, epsilon ' + str(e))
        plt.show()

    num_bach = num_bachelors(adult)
    plot_error(num_bach, 1)

if __name__ == '__main__':
    main()