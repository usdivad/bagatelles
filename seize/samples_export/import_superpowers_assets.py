#!/usr/bin/env python

'''
Batch Importer + Updater for Superpowers Assets
- David Su (http://usdivad.com/)

This is mostly for my personal use (for importing/updating audio assets),
but it might prove useful for others as well.

Check out the comment block above the main method for instructions!
'''

import copy
import json
import os
import re
from shutil import copyfile
import sys

# directory name -> asset id
def get_asset_id_from_filename(asset_name):
    found = re.search(r'(?<=\()\d+(?=\))', asset_name)
    id = found.group(0) if found else None
    return id

# asset entry (making use of name and id) -> directory name
def asset_entry_to_path(asset_entry):
    return '{} ({})'.format(asset_entry['name'], asset_entry['id'])

# traverse entries using DFS to find asset entry, else return None
# this also adds the path to the directory containing the asset
def get_asset_entry(entries, asset_name, original_path):
    asset_entry = None
    # print original_path
    for entry in copy.deepcopy(entries):
        if entry['name'] == asset_name:
            entry['path_to_destination_parent'] = original_path
            asset_entry = entry
        elif 'children' in entry:
            path = original_path + '/' + asset_entry_to_path(entry)
            asset_entry = get_asset_entry(entry['children'], asset_name, path)
    return asset_entry

# find highest entry id using DFS
def get_highest_entry_id(entries, highest):
    for entry in entries[:]:
        if int(entry['id']) > highest:
            highest = int(entry['id'])
        if 'children' in entry:
            highest = get_highest_entry_id(entry['children'], highest)
    return highest

# add new entry to entries in the spot dictated by parent id list
def add_entry(new_entry, entries, parent_id_list=[]):
    if len(parent_id_list) < 1:
        entries.append(new_entry)
        print new_entry
        return entries

    id = parent_id_list.pop(0)

    for i, entry in enumerate(entries, start=0):
        if entry['id'] == str(id):
            if 'children' in entry:
                entry['children'] = add_entry(new_entry, entry['children'], parent_id_list)
            else:
                print 'Error: ID {} in parent_id_list has no children. Should it be the last element of the list?'.format(id)
                # return entries

    return entries

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
    if asset_settings['update_json']:
        with open(json_path, 'w') as f:
            f.write(asset_settings['json'])

    print 'success!\n'

'''
To use this you should change the properties in user_params:

1. Update 'path_source' to point to the directory containing the assets you wish to import.
2. Update 'path_project' to point to where your Superpowers project lives.
   If you are adding new assets (i.e. creating files and updating entries.json):
        a. Update 'path_destination_relative' to point to the destination directory you'd like to create the asset files in.
        b. Update 'entry_parent_id_list' to contain a list of IDs of successive children that lead to your destination in entries.json.
3. Change the asset type, extension, JSON string, and valid source extensions to import.
   NOTE: You can set 'update_json' to False if you wish to retain your previous asset JSON files.
'''
if __name__ == '__main__':
    path_source_relative = sys.argv[1] # e.g. "guitar_intro"
    path_destination_relative = sys.argv[2] # e.g. "Audio (14)/Instrumental Entrance (37)"
    entry_parent_id_list = [int(x) for x in sys.argv[3].split(",")] # e.g. "14,37"; corresponds to the above

    # things you should adjust
    user_params = {
        'path_source': '/Users/usdivad/Documents/music/bagatelles/seize/samples_export/' + path_source_relative,
        'path_project': '/Users/usdivad/Library/Superpowers/projects/seize',
        'path_destination_relative': '/' + path_destination_relative,
        'entry_parent_id_list': entry_parent_id_list,

        'asset_valid_source_extensions': ['mp3'],

        'asset_type': 'sound',
        'asset_extension': 'dat',
        'asset_json': '{\n  "formatVersion": 1,\n  "streaming": false\n}',
        'asset_update_json': True
    }

    # paths
    path_source = user_params['path_source']
    path_project = user_params['path_project']
    path_project_entries = path_project + '/entries.json'
    path_project_assets = path_project + '/assets'
    path_destination = path_project_assets + user_params['path_destination_relative']

    # file settings
    valid_source_extensions = user_params['asset_valid_source_extensions']
    asset_settings = {
        'type': user_params['asset_type'],
        'extension': user_params['asset_extension'],
        'json': user_params['asset_json'],
        'update_json': user_params['asset_update_json'],
        # 'path_to_assets': path_project_assets
    }

    # entries
    entries = []
    highest_id = 0
    entry_parent_id_list = user_params['entry_parent_id_list'] # essentially functions as a linked list
    with open(path_project_entries, 'r') as f:
        entries = json.loads(f.read())

    # test_entry = get_asset_entry(entries, 'A1', '')
    # copy_asset_files(test_entry, asset_settings)
    # print test_entry

    highest_id = get_highest_entry_id(entries, 0)
    print 'highest id: {}'.format(highest_id)

    # assets
    if not os.path.isdir(path_source):
        print 'invalid "from" directory'
        exit(1)

    for asset_name in os.listdir(path_source):
        # check validity
        asset_is_valid = False
        for ext in valid_source_extensions:
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
                    # 'path_to_source': path_source + '/' + asset_name,
                    'path_to_destination_parent': path_destination
                }

                # add to entries.json
                entries = add_entry({
                    'id': str(asset_entry['id']),
                    'name': asset_entry['name'],
                    'type': asset_entry['type']
                }, entries[:], entry_parent_id_list[:])
            else:
                print 'asset {} exists'.format(asset_name)


            # copy the asset data and json files
            asset_entry['path_to_source'] = path_source + '/' + asset_name
            copy_asset_files(asset_entry, asset_settings)

    # write to entries.json
    with open(path_project_entries, 'w') as f:
        f.write(json.dumps(entries, indent=2, sort_keys=True))

    print 'done'


    # for filename in os.listdir(path_destination):
    #     filepath_full = path_destination+'/'+filename
    #     print get_asset_id_from_filename(filename)
    #     print os.path.isdir(filepath_full)