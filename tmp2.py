from nltk import find
from numpy import *
import matplotlib
import matplotlib.pyplot as plt
from numpy.random import rand
import numpy as np
import csv

def read_user_results_csv(csv_path):
    f = open(csv_path)
    reader = csv.reader(f)
    headers = next(reader, None)

    users = []
    for row in reader:
        user = dict()
        for h, v in zip(headers, row):
            user[h] = v
            # columns[h].append(v)
        users.append(user)
    # print(columns)
    print(users)

    columns = {}

    for h in headers:
        columns[h] = []

    for row in reader:
        for h, v in zip(headers, row):
            columns[h].append(v)
    print(len(columns))

    headers = []
    for h in columns:
        if len(str(h)) == 0:
            continue
        headers.append(h)

    return headers, users


x = rand(50, 30)
# basic
f1 = plt.figure(1)
plt.subplot(211)
plt.scatter(x[:, 1], x[:, 0])

# with label
plt.subplot(212)
label = list(ones(20)) + list(2 * ones(15)) + list(3 * ones(15))
label = array(label)
plt.scatter(x[:, 1], x[:, 0], 15.0 * label, 15.0 * label)


plt.show()

# with legend
f2 = plt.figure(2)
idx_1 = np.where(label == 1)
p1 = plt.scatter(x[idx_1, 1], x[idx_1, 0], marker='x', color='m', label='1', s=30)
idx_2 = np.where(label == 2)
p2 = plt.scatter(x[idx_2, 1], x[idx_2, 0], marker='+', color='c', label='2', s=50)
idx_3 = np.where(label == 3)
p3 = plt.scatter(x[idx_3, 1], x[idx_3, 0], marker='o', color='r', label='3', s=15)
plt.legend(loc='upper right')
plt.show()
