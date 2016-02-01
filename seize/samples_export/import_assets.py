import json
import os
import re
from shutil import copyfile

def get_asset_id_from_filename(asset_name):
    found = re.search(r'(?<=\()\d+(?=\))', asset_name)
    id = found.group(0) if found else None
    return id

def asset_entry_to_path(asset_entry):
    return '{} ({})'.format(asset_entry['name'], asset_entry['id'])

# traverse entries using DFS to find asset entry, else return None
# this also adds the path to the directory containing the asset
def get_asset_entry(entries, asset_name, original_path):
    asset_entry = None
    # print original_path
    for entry in entries:
        if entry['name'] == asset_name:
            entry['path_to_destination_parent'] = original_path
            asset_entry = entry
        elif 'children' in entry:
            path = original_path + '/' + asset_entry_to_path(entry)
            asset_entry = get_asset_entry(entry['children'], asset_name, path)
    return asset_entry

# find highest entry id using DFS
def get_highest_entry_id(entries, highest):
    for entry in entries:
        if int(entry['id']) > highest:
            highest = int(entry['id'])
        if 'children' in entry:
            highest = get_highest_entry_id(entry['children'], highest)
    return highest

# copy asset data and json files
def copy_asset_files(asset_entry, asset_settings):
    print 'copying asset ' + asset_entry['name']
    print asset_entry
    src_path = asset_entry['path_to_source']
    dst_path = asset_entry['path_to_destination_parent'] + '/' + asset_entry_to_path(asset_entry)
    data_filename = '{}.{}'.format(asset_settings['type'], asset_settings['extension'])
    json_filename = asset_settings['type'] + '.json'
    data_path = dst_path + '/' + data_filename
    json_path = dst_path + '/' + json_filename
    # print dst_path

    # create destination directory if necessary
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    # copy asset data
    copyfile(src_path, data_path)

    # write asset json
    with open(json_path, 'w') as f:
        f.write(asset_settings['json'])

    print 'success!\n'

if __name__ == '__main__':
    # paths
    path_source = '/Users/usdivad/Documents/music/bagatelles/seize/samples_export/guitar_intro'
    path_project = '/Users/usdivad/Library/Superpowers/projects/seize'
    path_project_entries = path_project + '/entries.json'
    path_project_assets = path_project + '/assets'
    path_destination = path_project_assets + '/Audio (14)/Guitar Intro (15)'

    # file settings
    valid_extensions = ['mp3']
    asset_settings = {
        'type': 'sound',
        'extension': 'dat',
        'json': '{\n  "formatVersion": 1,\n  "streaming": false\n}',
        'path_to_assets': path_project_assets
    }

    # entries
    entries = []
    highest_id = 0
    entry_parent_list = ['Audio', 'Guitar Intro']
    with open(path_project_entries, 'r') as f:
        entries = json.loads(f.read())

    highest_id = get_highest_entry_id(entries, 0)

    test_entry = get_asset_entry(entries, 'A1', '')
    # copy_asset_files(test_entry, asset_settings)

    print test_entry
    print highest_id

    # assets
    if not os.path.isdir(path_source):
        print 'invalid "from" directory'
        exit(1)

    for asset_name in os.listdir(path_source):
        # check validity
        asset_is_valid = False
        for ext in valid_extensions:
            if asset_name.endswith(ext):
                asset_is_valid = True

        # create or update the asset in the superpowers project
        if asset_is_valid:
            # print asset_name
            asset_entry = get_asset_entry(entries, asset_name, path_project_assets)
            
            if not asset_entry:
                asset_id = highest_id + 1
                highest_id = asset_id

                asset_entry = {
                    'id': asset_id,
                    'name': asset_name,
                    'type': asset_settings['type'],
                    'path_to_destination_parent': path_destination
                }

                # add to entries.json


            # copy the asset data and json files
            asset_entry['path_to_source'] = path_source + '/' + asset_name
            copy_asset_files(asset_entry, asset_settings)


    # for filename in os.listdir(path_destination_full):
    #     filepath_full = path_destination_full+'/'+filename
    #     print get_asset_id_from_filename(filename)
    #     print os.path.isdir(filepath_full)