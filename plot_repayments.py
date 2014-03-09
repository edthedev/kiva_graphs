#!/usr/bin/env python
import os
import simplejson
import collections
import subprocess
import matplotlib.pyplot as plt

USERNAME = 'edandjoani'
IMAGE_ROOT = 'images'

DOWNLOAD_LOAN_DATA = True
BUILD_GRAPHS = False

if DOWNLOAD_LOAN_DATA:

    files = os.listdir('.')
    for filename in files:
        if not USERNAME in filename:
            continue

# Create this file by calling curl_list_loans.sh USERNAME
        f = open(USERNAME + '.json', 'r')
        raw_data = f.read()
        f.close()

# Call other curl to download loan data for all loans.
        print "Downloading all loan data..."
        dataset = simplejson.loads(raw_data)
        loans = dataset['loans']
        for loan_id in loans:
            subprocess.call('./curl_kiva.sh %d' % loan_id, shell=True)
            print "Downloaded %d." % loan_id
        # TODO: Ask for the next page, when we reach the end.

if BUILD_GRAPHS:
# Make graphs for all loans.
    print "Creating graphs for all loans."
    files = os.listdir('.')
    for filename in files:

        if not '.json' in filename:
            continue
        if filename == '.json':
            continue
        if filename == USERNAME + '.json':
            continue

# Create this file by calling curl_list_loans.sh USERNAME
        f = open(filename, 'r')
        raw_data = f.read()
        f.close()

        dataset = simplejson.loads(raw_data)
        import pdb; pdb.set_trace()
# Assume one loan
        loan = dataset['loans'][0]
# Assume one borrower
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
        plt.savefig(IMAGE_ROOT + '/' + name + '.jpg')
        print "Create graph %s.jpg" % name

# import pdb; pdb.set_trace()
