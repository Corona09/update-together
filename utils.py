#!/usr/bin/env python
import os, json

class Result(object):

    def __init__(self, status=True, message=None):
        self.status = status
        self.message = message

def run_cmd(cmd):
    """
    执行 shell 命令
    @param cmd 命令
    """
    status = os.system(cmd)
    return True if status == 0 else False

def is_git_repo(folder):
    """
    检查一个目录是否是 git 仓库
    """
    status = run_cmd(f"cd {folder} && git rev-parse --is-inside-work-tree > /dev/null 2>&1")
    if not status:
        return False
    return status

def get_remote_origin_name(repo):
    """
    获取远程仓库的名称
    @return 仓库名称/None
    """
    cmd = f"cd {repo} && " + r"git remote -v | awk -F ' ' 'NR==1{print $1}'"
    name = os.popen(cmd).read()
    return name if name else None

def is_git_repo_out_of_date(repo):
    """
    检查一个 git 仓库是否过时
    在执行该函数前需对 repo 使用 is_git_repo 函数进行判定, 以确保指定的确实是一个 git repo
    @return 有更新返回 True, 无更新返回 False
    """

    origin = get_remote_origin_name(repo=repo)

    # 若无远程仓库, 直接返回 False, 无需更新
    if not origin:
        return False

    cmd = f"cd {repo} && git fetch {origin}"

    result = os.popen(cmd=cmd).readlines()

    return True if result else False

def read_repo_opts(config_json_file):
    """
    读取设置, 
    """
    if os.path.exists(config_json_file):
        fp = open(config_json_file, 'r', encoding='utf-8')
        data = dict(json.load(fp=fp))
        return data
    else:
        return None

