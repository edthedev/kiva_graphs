#!/usr/bin/env python
import os
import simplejson

import matplotlib.pyplot as plt

files = os.listdir('.')

for filename in files:
    if not '.json' in filename:
        continue
    f = open(filename, 'r')
    raw_data = f.read()
    f.close()

    dataset = simplejson.loads(raw_data)

# Assume one loan
    loan = dataset['loans'][0]

    paid = {}
    for payment in loan['payments']:
        paid[ payment['processed_date'] ] = payment['amount']

    print paid
    import pdb; pdb.set_trace()

    # plt.plot([1,2,3,5])
    plt.bar(range(len(paid)),
            paid.values(), align='center')
    plt.xticks(range(len(paid)), paid.keys())

    plt.ylabel('Dollars repaid')
    plt.xlabel('Name of Lendee')
    plt.show()

