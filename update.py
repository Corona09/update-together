#!/usr/bin/env python

import os
from utils import is_git_repo_out_of_date, run_cmd, Result, is_git_repo
import utils

"""
全面更新系统
1. 更新系统: sudo dnf --refresh upgrade -y
2. 更新 flatpak: http_proxy=http://127.0.0.1:7890 flatpak update -y
3. 更新 pip: pip update
4. 更新 cargo:
5. 更新 npm
6. 更新固件（选）
7. 更新指定目录 git 仓库并执行相关命令
"""

def update_system():
    """
    更新系统
    执行 `dnf --refresh update -y`
    成功返回 True; 失败返回 False
    """
    status = run_cmd('sudo dnf --refresh upgrade -y')
    return Result(status=status)

def update_flatpak():
    """
    更新 flatpak 软件
    执行 `flatpak update -y`
    成功返回 True; 失败返回 False
    """
    proxy="http://127.0.0.1:7890"
    env = f'http_proxy={proxy} https_proxy={proxy}'
    cmd = f'bash -c "{env} flatpak update -y"'
    status = run_cmd(cmd=cmd)
    return Result(status=status)

def update_pip():
    status = run_cmd('python3 -m pip install --upgrade pip')
    if not status:
        return False

    pip_pkgs = os.popen('pip list --outdated').readlines()
    for pkg in pip_pkgs[2:]:
        run_cmd(f'pip install --upgrade {pkg.split()[0]}')


    # 更新全局包
    pip_pkgs_global = os.popen('sudo pip list --outdated').readlines()
    for i in range(len(pip_pkgs_global)):
        if pip_pkgs_global[i].startswith('---'):
            pip_pkgs_global = pip_pkgs_global[i+1:]
            break

    for pkg in pip_pkgs_global:
        run_cmd(f'sudo pip install --upgrade {pkg.split()[0]}')

    return Result()

def update_cargo():
    status = run_cmd('cargo install-update -a')
    return status

def update_npm():
    status = run_cmd('sudo npm update -g')
    return status

def update_git_repo(use_proxy, folder, cmd=None):
    """
    @param use_proxy 为 None 或 False 时不使用代理，否则使用代理
    """
    proxy = "http://127.0.0.1:7890"
    env = "" if not use_proxy else f"http_proxy={proxy} https_proxy={proxy}"

    if not is_git_repo(folder=folder):
        return Result(status=False, message=f"{folder} 不是一个 git 仓库.")

    if not is_git_repo_out_of_date(repo=folder):
        return Result(status=True, message=f"{folder} 不需要更新")

    print(f"\n更新 {folder}...\n")

    return

    status = run_cmd(f'cd {folder} && {env} git pull')

    if status and cmd:
        if type(cmd) == type([]):
            for c in cmd:
                status = run_cmd(f'cd {folder} && {c}')
                if not status:
                    print(f'Error while executing {c}.')
                    break
        else:
            status = run_cmd(f'cd {folder} && {cmd}')
    return Result(status=status)

