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
# Assume one borrower
    name = loan['borrowers'][0]['first_name']
# Loan amount
    total_loaned = loan['terms']['disbursal_amount']

# Gather up distributions
    paid_out = {}
    for payment in loan['terms']['local_payments']:
        paid_out[ payment['due_date'] ] = payment['amount']

# Gather up payments
    paid = {}
    total_paid = 0
    for payment in loan['payments']:
        total_paid += payment['amount']
        paid[ payment['processed_date'] ] = total_paid

# Graph distributions 
    #plt.bar(range(len(paid_out)),
    #        paid_out.values(), align='center')
    

# Graph payments
    plt.bar(range(len(paid)),
            paid.values(), align='center')

# Label graph
    plt.xticks(range(len(paid)), paid.keys())
    plt.ylabel('Dollars repaid')
    # plt.yticks(range(0, total_loaned), range(0, total_loaned, 100))
    plt.axis([0, len(paid), 0, total_loaned])
    plt.xlabel(name)
    plt.show()

    # import pdb; pdb.set_trace()
