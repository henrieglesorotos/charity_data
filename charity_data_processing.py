import pandas as pd
import logging
import re
import os

logging.basicConfig(level=logging.INFO)

control_group = '102', '113', '201'
main_columns = 'regno', 'subno' ,'name', 'orgtype', 'postcode', 'phone'

def processing():

    # reading the class lookup table
    logging.info('importing class table')
    control = pd.read_csv('extracts/extract_class.csv', dtype={'regno': object, 'class': object})

    # reading main charity table.
    logging.info('importing main charity table')
    main = pd.read_csv('extracts/extract_charity.csv', usecols = main_columns, dtype={'regno': object})

    # reading other main charity table
    logging.info('charity table without subsidiaries. we are removing subsidiaries. includes email/web')
    legit = pd.read_csv('extracts/extract_main_charity.csv', usecols=['regno', 'income', 'email', 'web'],
                        dtype={'regno': object})

    # reading area of business table
    logging.info('importing area of operation table')
    aoo = pd.read_csv('extracts/extract_charity_aoo.csv', dtype={'regno': object, 'aookey': object})
    aoo_ref = pd.read_csv('extracts/extract_aoo_ref.csv', dtype={'aookey': object})

    # reading charitable purposes
    logging.info('importing charitable purpose info')
    purpose = pd.read_csv('extracts/extract_objects.csv', usecols=['regno', 'subno', 'seqno', 'object'], dtype={'regno': object,
                                                                                                                'subno': object, 'seqno': object})

    logging.info('processing charitable purpose data to only include the original charitable purpose')
    purpose = purpose[purpose['subno'] == '0']
    purpose = purpose[purpose['seqno'] == '0000']
    purpose = purpose.drop(['subno', 'seqno'], axis=1)

    clean_purpose(purpose)

    # add charitable purposes
    logging.info('merging chritable purposes to original file')
    main = main.merge(purpose, on='regno', how='left')

    # adding class, web, email, income information, removing stupid subsidiaries
    logging.info('removing subsidiaries')
    main = main[main['subno'] == 0]
    logging.info('filtering for charities of interest')
    main = main.merge(control, left_on='regno', right_on='regno', how='left')
    main = main.merge(legit, left_on='regno', right_on='regno', how='inner')

    # add location data
    logging.info('adding location data')
    main = main.merge(aoo, left_on='regno', right_on='regno', how='left')

    # add reference data
    logging.info('adding areas of business')
    main = main.merge(aoo_ref, on=['aootype', 'aookey', 'welsh', 'master'], how='left')
    main = main.drop(['aootype', 'aookey', 'welsh', 'master', 'aooname'], axis=1)

    # group the locations are there are multiple
    logging.info('concatenate the areas of business')
    main = main.groupby(['regno','subno','name','orgtype','postcode',
                         'phone','class','income','email','web', 'object'], as_index=False).aggregate(lambda x: list(x))

    # deal with telephone numbers in excel
    logging.info('putting @ at start of phone numbers so they play nicely in excel')
    main['phone'] = '@' + main['phone']

    # only have current registered charities
    main = main[main['orgtype'] == 'R']

    output_data(main)

def clean_purpose(purpose):
    logging.info('removing non-alphanumeric from purpose statements so it works with .csv')
    purpose['object'] = [re.sub('[,]+', '', str(x)) for x in purpose['object']]
    purpose['object'] = [re.sub('\s+', ' ', str(x)) for x in purpose['object']]
    purpose['object'] = [x[0:150] for x in purpose['object']]
    return purpose

def output_data(main):
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    for idx, i in enumerate(control_group):
        logging.info(f'This is sequence {idx}: {i}')
        output = main[main['class'] == i]
        output.to_csv(f'outputs/output_{i}.csv', index=False)

processing()










