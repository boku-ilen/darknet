import json
import os.path

FILE_PATH = '../../../../../Praktikum_data/workshops/'
ALL_DATA = 'all_data/'

# uncomment for parsing location.impression
VECTORS = 'vectors/vectors_'

# uncomment for parsing assetpos/assetpositions
#VECTORS = 'assetpos/assetpositions_'

FILENAME = '0.01-191415.json'
REPLACE_LAST_OCCURRENCE = ', {"model"'


# vector data example:
# {'model': 'location.impression', 'pk': 1, 'fields': {'session': 1,
# 'location': 'SRID=3857;POINT Z (-1535903 5911750 0)', 'viewport':
# 'SRID=3857;POINT Z (0.866019 -0.500011 0)', 'timestamp': '2019-08-08T23:31:07.026Z'}}


def read_json():
    with open(FILE_PATH + ALL_DATA + FILENAME, 'r') as workshop_file:
        return workshop_file.read()


# save vector data as json file if does not exists yet
def save_json(data_obj):
    vector_data = []
    for idx in range(len(data_obj)):

        # uncomment for parsing location.impression
        if data_obj[idx]['model'] == 'location.impression':
            vector_data.append(data_obj[idx])

        # uncomment for parsing assetpos/assetpositions
        #if data_obj[idx]['model'] == 'assetpos.assetpositions':
            #if data_obj[idx]['fields']['asset_type'] != 1:
                #vector_data.append(data_obj[idx])

    filename = FILE_PATH + VECTORS + FILENAME
    if not os.path.isfile(filename):
        with open(filename, 'w') as file_write:
            json.dump(vector_data, file_write)
            print('JSON file saved: {}'.format(filename))
    else:
        print('did not save, the file already exists: {}'.format(filename))


# repair files: 0.01-094913.json, 0.01-095757.json, 0.01-100012.json
# which are not properly ended
# should end with: "}}]
# but end: 65962149)" or 97648208)" or }}, {"model"
# if error, find last ', {"model"' and replace with ']'
def repair_string(workshop_data):
    index = workshop_data.rfind(REPLACE_LAST_OCCURRENCE)
    new_string = workshop_data[:index] + ']'
    print('JSON file repaired')
    return new_string


# this code extracts vectors data from JSON and saves it again as a JSON file
workshop_string = read_json()
try:
    workshop_obj = json.loads(workshop_string)
    save_json(workshop_obj)
except ValueError:
    print('JSON File {} could not be parsed'.format(FILENAME))

    # if error, find last ', {"model"' and replace with ']'
    workshop_string = repair_string(workshop_string)
    try:
        workshop_obj = json.loads(workshop_string)
        save_json(workshop_obj)
    except ValueError:
        print('JSON File {} could not be repaired'.format(FILENAME))

