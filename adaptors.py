import re
import pandas as pd
import json


# create internal function that splits time into 'start' and 'end' times
def _times(a_string, index):
    # split string using re lib
    splits = re.split(r'[, :]', a_string)

    # cast to int each split
    splits = [int(a_split) for index, a_split in enumerate(splits) if index != 4]

    # calculate second start and end
    if index == 0:
        t = splits[0] * 3600 + splits[1] * 60 + splits[2] + splits[3]/1000
    elif index == 1:
        t = splits[4] * 3600 + splits[5] * 60 + splits[6] + splits[7]/1000
    else:
        t = -1

    return t


# youtube transform function
def youtube2df(filepath):
    # read the file
    with open(filepath) as f:
        file = f.read()

    # split the file
    lines = file.splitlines()

    # compress into tuples of three, ignoring 4th
    # tuples = [index, time, transcript]
    tps = [(lines[i], _times(lines[i + 1], 0), _times(lines[i + 1], 1), lines[i + 2]) for i in range(0, len(lines), 4)]

    # convert to dataframe
    _df = pd.DataFrame(tps, columns=['orig_index', 'start', 'end', 'transcript'])

    return _df


# AWS function with filepath to json function
def aws2df(filepath):

    # read the file
    with open(filepath) as f:
        data = json.load(f)

    # compress into tuples
    tuples = []
    for value in data['results']['items']:
        if value.get('start_time'):
            tuples.append((value.get('start_time'),
                           value.get('end_time'),
                           value['alternatives'][0].get('content')
                           ))

    # transform to df
    _df = pd.DataFrame(tuples, columns=['start', 'end', 'transcript'])

    return _df
