__author__ = 'arashiyama'
import json
from pprint import pprint
import urllib2
from dateutil.parser import *
from datetime import datetime, date, time
from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

############################## GLOBALS ########################################
STREAM_HASH = '' # insert your datasift stream hash here
Base = declarative_base()
############################## CLASSES ########################################
class Bucket(Base):
    __tablename__ = 'sandpit'

    id = Column(Integer, primary_key=True)
    handle = Column(String(50))
    counter= Column(Integer)

    def __init__(self, handle, counter):
        self.handle = handle
        self.counter = counter

    def __repr__(self):
        return "<Bucket('%s', '%d')>" % (self.handle, self.counter)

####################################### helpers ##############################

def get_bucket_name(twee,dtstamp):
    dt = parse(dtstamp)
    bucket = "bucket-%s-%s" % (twee,dt.strftime('%Y%b%d%H%M'))
    return bucket

"""
# How to use:

complicated_dict = {"dict1key": {"dict2key": [{"dict3key": {"tell":"me"}}]}}
one_level_dict = makeSimpleDict(complicated_dict)
print one_level_dict
# prints out {'dict1key.dict2key.[0].dict3key.tell': u'me'}
"""
def makeSimpleDict(complex_dict):
    """
    @param complex_dict : a python dict that might have inner dicts and arrays OR
    a python list that might have inner dicts and arrays OR
    a python object that's neither list of dict

    @return plain_dict : plain dict that has only one level or a plain python object
    """
    # make plain dict that you will return
    plain_dict = {}

    if isinstance(complex_dict, dict):
        # if complex_dict is a dict
        # loop through the keys of this complex dict
        sawComplex = False
        for complex_key in complex_dict:
            # if complex_dict[complex_key] is a dict
            if isinstance(complex_dict[complex_key], dict):
                sub_dict = complex_dict[complex_key]
                # loop through the keys of this sub_dict
                sawComplex = True
                for sub_key in sub_dict:
                    plain_dict[complex_key+"."+sub_key] = makeSimpleDict(sub_dict[sub_key])
            elif isinstance(complex_dict[complex_key], list):
                if not isComplexList(complex_dict[complex_key]):
                    plain_dict[complex_key] = getStrFromList(complex_dict[complex_key])
                else:
                    sawComplex = True
                    for i in range(len(complex_dict[complex_key])):
                        plain_dict[complex_key+"["+str(i)+"]"] = makeSimpleDict(complex_dict[complex_key][i])
            else:
                plain_dict[complex_key] = makeSimpleDict(complex_dict[complex_key])
        if sawComplex:
            return makeSimpleDict(plain_dict)
        else:
            return plain_dict
    else:
        # if not a dict
        if isinstance(complex_dict, list):
            # if complex_dict is a list

            # is complex_dict a list
            # that contains a dict or an inner list?
            if not isComplexList(complex_dict):
                accum = getStrFromList(complex_dict)
                plain_dict = accum
            else:
                # loop through the complex_dict
                for i in range(len(complex_dict)):
                    plain_dict["["+str(i)+"]"] = makeSimpleDict(complex_dict[i])
            return makeSimpleDict(plain_dict)
        else:
            # if neither a list nor a dict
            return unicode(complex_dict)


def isComplexList(ls):
    for each in ls:
        if isinstance(each, dict) or isinstance(each, list):
            return True
    return False

def getStrFromList(ls):
    if isinstance(ls, list):
        return ", ".join([unicode(each) for each in ls])
    else:
        return ls

def fill_a_bucket(bucket_name):
    # We need to check if the bucket exists, if it does, increment the counter
    row = session.query(Bucket).filter(Bucket.handle == bucket_name)
    if len(row.all()) == 0:
        # no bucket exists, so create it with a counter of 1
        red_bucket = Bucket(bucket_name, 1)
        session.add(red_bucket)
        print("Created a new red bucket with name %s" % bucket_name)
    elif len(row.all()) == 1:
        # We have an existing bucket so increment it
#        print("If I only knew how to increment the counter for %s which is currently %d" % (row.handle, row.counter))
        row.update({Bucket.counter: Bucket.counter + 1})
        print("I think I added 1 to bucket %s" % bucket_name)
    else:
        # This is an error as we have more than one bucket with the same name. Karmically bad!
        logging.error("More than one bucket found with bucket_name set to %s" % bucket_name)
    # Commit to the database, feel good about ourselves for a microsecond, then get the next one
    session.commit()

############################### MAIN ########################################
def DSLoop(hash=STREAM_HASH):
    ds_url = r'https://stream.datasift.com/'+hash
    ds_data = r'' # Insert your authorisation keys
    request = urllib2.Request(ds_url, headers={'Authorization':ds_data})
    for l in urllib2.urlopen(request):
        the_data = makeSimpleDict(json.loads(l))
        logging.debug("number of twitter fields received: %d" % len(the_data.keys()))
        for i in sorted(the_data.keys()):
            if r'twitter.created_at' in i:
                bucket_name = get_bucket_name("TWT",the_data[i])
                fill_a_bucket(bucket_name)
            if r'retweet.created_at' in i:
                bucket_name = get_bucket_name("RT",the_data[i])
                fill_a_bucket(bucket_name)


if __name__=="__main__":
    # set up data base
    db = create_engine('sqlite:///DSdata.sqlite')
    Session = sessionmaker(bind=db)
    session = Session()
    Base.metadata.create_all(db)
    # bind data to classes
    DSLoop(STREAM_HASH)
