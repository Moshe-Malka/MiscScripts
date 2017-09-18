# Moshe Malka
import time
import random
import string

def checkDict(prevDict,in_dict):
    ''' Function to check if the data is new, and if so - send it and update the previous state.'''
    # get symmetric diff of the 2 dictionaries:
    sym_diff = set(prevDict.items()).symmetric_difference(in_dict.items())
    diff = dict(sym_diff & set(in_dict.items()))
    if(len(diff)):       # True - there is a new value
        print "--->      Found {0} Changes.".format(len(diff))
        print "Old Dictionery : {}".format(prevDict)
        print "New Dictionery : {}".format(in_dict)
        print "Sending Changes (Diff) : {}".format(diff)
        print "["+"#"*80+"]"
        sendDict(diff)       # sending only the changes.
        return in_dict      # returning the new dictionery to be saved as the previous data.
    else:
        return prevDict

def sendDict(d):
    ''' Placeholder for the function that sends the message to the server'''
    pass

def getRandomDict():
    ''' Returns a dictionery with 5 Keys (1-5) and random characters. --- for testing purposes --- '''
    return {n: ''.join(random.choice(string.ascii_uppercase)) for n in range(1,6)}

def main():
    prevDict = {}
    while True:
        prevDict = checkDict(prevDict,getRandomDict())
        time.sleep(1)

if __name__ == "__main__":
    main()
