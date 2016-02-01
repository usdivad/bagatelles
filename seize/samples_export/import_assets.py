import json
import os
import re
from shutil import copyfile

def get_asset_id(asset_name):
    found = re.search(r'(?<=\()\d+(?=\))', asset_name)
    id = found.group(0) if found else None
    return id

if __name__ == '__main__':
    # paths
    dir_from = '/Users/usdivad/Documents/music/bagatelles/seize/samples_export/guitar_intro'
    dir_project_assets = '/Users/usdivad/Library/Superpowers/projects/seize/assets'
    dir_to = dir_project_assets + '/Audio (14)/Guitar Intro (15)'

    # types
    valid_extensions = ['mp3']
    asset_type = 'sound'
    asset_extension = 'dat'
    asset_json = '{\n  "formatVersion": 1,\n  "streaming": false\n}'

    if not os.path.isdir(dir_from):
        print 'invalid "from" directory'
        exit(1)

    for asset in os.listdir(dir_from):
        asset_is_valid = False
        for ext in valid_extensions:
            if asset.endswith(ext):
                asset_is_valid = True
        if asset_is_valid:
            print asset


    # for filename in os.listdir(dir_to_full):
    #     filepath_full = dir_to_full+'/'+filename
    #     print get_asset_id(filename)
    #     print os.path.isdir(filepath_full)