import os
from update import *
from utils import read_repo_opts

HOME = os.getenv('HOME')
default_config_file = os.path.join('.', 'config.json')

conf = read_repo_opts(default_config_file)

if not conf:
    print(f"Error when loading config.json")
    exit(1)

git_repos = conf['git']

for item in git_repos:
    path = item['path']
    if 'cmds' in item.keys():
        cmds = item['cmds']
    else:
        cmds = None

    if 'proxy' in item.keys():
        proxy = bool(item['proxy'])
    else:
        proxy = True

    update_git_repo(use_proxy=proxy, folder=path, cmd=cmds)
