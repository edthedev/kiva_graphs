#!/usr/bin/env python
"""plot_repayments.py

Usage:
  plot_repayments.py download <username>
  plot_repayments.py plot DATAFILE [--data=FOLDER] [--images=FOLDER]
  plot_repayments.py plotall [--data=FOLDER] [--images=FOLDER]
  plot_repayments.py (-h | --help)
  plot_repayments.py --version

Options:
  --data=FOLDER       The data directory [default: ./data]
  --images=FOLDER       The data directory [default: ./images]
  -h --help     Show this screen.
  --version     Show version.

"""

SCRATCH = """


"""
import os
import simplejson
import collections
import subprocess
import matplotlib.pyplot as plt

import docopt

IMAGE_ROOT = 'images'
BUILD_GRAPHS = False

from docopt import docopt


def download_loan_data(user_filename):

# Create this file by calling curl_list_loans.sh USERNAME
        f = open(filename, 'r')
        raw_data = f.read()
        f.close()

# Call other curl to download loan data for all loans.
        print "Downloading all loan data..."
        dataset = simplejson.loads(raw_data)
        loans = []
        if 'loans' in dataset.keys():
            loans = dataset['loans']
        else:
            print "Unable to process " + filename

        for loan_id in loans:
# Be polite to the remote server...
            sleep(1)

            subprocess.call('./curl_kiva.sh %d' % loan_id, shell=True)
            print "Downloaded %d." % loan_id
        # TODO: Ask for the next page, when we reach the end.

def plot(filename):
    ''' Plot the data from the file. '''

# Create this file by calling curl_list_loans.sh USERNAME
    if not os.path.exists(filename):
        print "File %s does not exist." % filename
        return False

    f = open(filename, 'r')
    raw_data = f.read()
    f.close()

    dataset = simplejson.loads(raw_data)
# Assume one loan
    if not 'loans' in dataset:
        print "Unable to process " + filename
        return False

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
    repaid = {'': 0}
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

def build_graphs(DATA_DIR, IMAGE_ROOT):
    ''' Convert all load data found in the data dir into graph files.'''

# Make graphs for all loans.
    print "Creating graphs for all loans."
    files = os.listdir(DATA_DIR)
    for filename in files:

        if not '.json' in filename:
            continue
        if filename == '.json':
            continue
        if USERNAME in filename:
            continue

        plot(filename)

if __name__ == '__main__':
    args = docopt(__doc__, version='Kiva Loan Plots 0.2')
    print(args)
    USERNAME = args['<username>']
    DATA_DIR = args['--data']
    IMAGE_ROOT = args['--images']
    if args['plotall']:
        pass
        build_graphs(DATA_DIR, IMAGE_ROOT)

    if args['plot']:
        plot(args['DATAFILE'])

    if args['download']:
        files = os.listdir(DATA_DIR)
        for filename in files:
            if not USERNAME in filename:
                continue
            download_loan_data(filename)

