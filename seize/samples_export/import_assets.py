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
            entry['path'] = original_path
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

if __name__ == '__main__':
    # paths
    path_source = '/Users/usdivad/Documents/music/bagatelles/seize/samples_export/guitar_intro'
    path_project = '/Users/usdivad/Library/Superpowers/projects/seize'
    path_project_entries = path_project + '/entries.json'
    path_project_assets = path_project + '/assets'
    path_destination = path_project_assets + '/Audio (14)/Guitar Intro (15)'

    # types
    valid_extensions = ['mp3']
    asset_type = 'sound'
    asset_extension = 'dat'
    asset_json = '{\n  "formatVersion": 1,\n  "streaming": false\n}'

    # entries
    entries = []
    highest_id = 0
    with open(path_project_entries, 'r') as f:
        entries = json.loads(f.read())

    highest_id = get_highest_entry_id(entries, 0)

    print get_asset_entry(entries, 'A1', '')
    print highest_id

    # assets
    if not os.path.isdir(path_source):
        print 'invalid "from" directory'
        exit(1)

    for asset in os.listdir(path_source):
        # check validity
        asset_is_valid = False
        for ext in valid_extensions:
            if asset.endswith(ext):
                asset_is_valid = True

        # create or update the asset in the superpowers project
        if asset_is_valid:
            print asset
            asset_entry = get_asset_entry(entries, asset, path_project_assets)
            
            if asset_entry: # modify existing asset
                print asset_entry['id']
            else: # create new asset





    # for filename in os.listdir(path_destination_full):
    #     filepath_full = path_destination_full+'/'+filename
    #     print get_asset_id_from_filename(filename)
    #     print os.path.isdir(filepath_full)