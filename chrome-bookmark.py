__author__ = 'dan'

import json
import os
from typing import List
from pprint import pprint

def read_json_file(filename: str) -> dict:
    with open(filename) as data_file:
        data = json.load(data_file)
        return data


def obtain_public_folders(chrome_bookmarks: dict, public_folders: List[str]) -> List[dict]:
    bookmark_bar_members = chrome_bookmarks.get('roots').get('bookmark_bar').get('children')
    public_folders_json = List()  # type : List
    for each in bookmark_bar_members:
        if each.get('name') in public_folders and each.get('type') == 'folder':
            public_folders_json.append(each)
    return public_folders_json

def write_publics_to_md(md_filename: str, publics: List[dict]) -> None:
    with open(md_filename, 'w') as md_output:
        for each in publics:
            md_output.write(generate_md_string(each, 0))
            md_output.write('\n')

def generate_md_string(json_node: dict, depth: int) -> str:

    if json_node.get('type') == 'url':
        return ''.join([('  '*depth), '* ', '[', json_node.get('name'), ']', '(', json_node.get('url'), ')', '\n'])

    string_list = List()  # type: List[str]
    string_list.append(('  '*depth) + '* ' + ('#' * min((depth+1)*2, 6)) + ' ' + json_node.get('name')+'\n')
    for each in json_node.get('children'):
        string_list.append(generate_md_string(each, depth+1))
    return ''.join(string_list)


if __name__ == '__main__':
    public_folders = ['Public']
    bookmark_file = '~/.config/google-chrome/Default/Bookmarks'
    export_target = '~/bookmarks.md'

    print('Loading bookmarks from {}'.format(os.path.expanduser(bookmark_file)))
    json_dict = read_json_file(os.path.expanduser(bookmark_file))
    public_json_folders = obtain_public_folders(json_dict, public_folders)
    write_publics_to_md(os.path.expanduser(export_target), public_json_folders)


