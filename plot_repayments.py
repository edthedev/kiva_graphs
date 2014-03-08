#!/usr/bin/env python
import os
import simplejson
import collections

import matplotlib.pyplot as plt

# files = os.listdir('.')

# for filename in files:

#    if not '.json' in filename:
#        continue

filename = 'edandjoani.json'

f = open(filename, 'r')
raw_data = f.read()
f.close()

dataset = simplejson.loads(raw_data)
loans = dataset['loans']
for loan in loans:
# Assume one loan
    loan = dataset['loans'][0]
# Assume one borrower
    import pdb; pdb.set_trace()
    name = loan['borrowers'][0]['first_name']
# Loan amount
    total_loaned = loan['terms']['disbursal_amount']

# Gather up distributions
#paid_out = {}
#for payment in loan['terms']['local_payments']:
#    paid_out[ payment['due_date'] ] = payment['amount']

# Gather up payments
    paid = {}
    for payment in loan['payments']:
        paid[ payment['processed_date'] ] = payment['amount']

# Get ready to chart total repaid over time
    repaid = {}
    total_paid = 0
    for day in sorted(paid.iterkeys(), reverse=True):
       total_paid += paid[day]
       repaid[day] = total_paid

# Graph distributions 
#plt.bar(range(len(paid_out)),
#        paid_out.values(), align='center')

# Graph payments
    plt.bar(range(len(repaid)),
            repaid.values(), align='center')

# Label graph
    plt.xticks(range(len(repaid)), repaid.keys())
    plt.ylabel('Dollars rerepaid')
# plt.yticks(range(0, total_loaned), range(0, total_loaned, 100))
    plt.axis([0, len(repaid), 0, total_loaned])
    plt.xlabel(name)
    # plt.show()
    plt.savefig(name + '.jpg')

# import pdb; pdb.set_trace()
