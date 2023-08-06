#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Copyright (C) 2011-2015 Matteo Bertini <matteo@naufraghi.net>
# Latest version: https://github.com/naufraghi/git-svn-clone-externals

from __future__ import absolute_import, division, print_function

import os
import sys
import argparse
import logging
import subprocess
from contextlib import contextmanager
from functools import wraps


logging.basicConfig(format='%(asctime)s %(levelname)s[%(name)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("git-svn-clone-externals")

class col:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

# subprocess helpers

@contextmanager
def cd(path):
    cur_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cur_dir)

@contextmanager
def lang(l):
    old_lang = os.environ["LANG"]
    os.environ["LANG"] = l
    yield
    os.environ["LANG"] = old_lang

def logged_call(func, log=logger.debug):
    @wraps(func)
    def _logged(args, **kwargs):
        color = col.BLUE
        if log is logger.info:
            color = col.GREEN
        elif log is logger.warning:
            color = col.YELLOW
        elif log is logger.error:
            color = col.RED
        end_color = col.ENDC
        cwd = os.getcwd()
        command = " ".join(args)
        log("{cwd}$ {color}{command}{end_color}".format(**locals()))
        res = func(args, **kwargs)
        if res and func is subprocess.call:
            color = col.RED
            logger.error("{cwd}$ {color}{command}{end_color}".format(**locals()))
        return res
    return _logged

sh = subprocess.check_output
lsh = logged_call(sh)

# Git svn helpers

@contextmanager
def git_stasher(path="."):
    with cd(path):
        git_status_lines = sh(["git", "status", "--por"]).strip().split()
        need_stash = any(l.startswith("M") for l in git_status_lines)
        if need_stash:
            lsh(["git", "stash"])
        yield
        if need_stash:
            lsh(["git", "stash", "pop"])

def git_svn_dcommit(path="."):
    with git_stasher(path):
        return lsh(["git", "svn", "dcommit"])

def git_svn_rebase(path="."):
    with git_stasher(path):
        return lsh(["git", "svn", "rebase"])

def git_svn_outgoing(path="."):
    with cd(path):
        dcommit_n_lines = lsh(["git", "svn", "dcommit", "-n"]).strip().split()
        diff_tree_lines = (l.startswith("diff-tree") for l in dcommit_n_lines)
        # diff-tree ff144a013554a3d9547e00ac37c1c349c932d874~1 ff144a013554a3d9547e00ac37c1c349c932d874
        for commit in (l.split()[-1] for l in diff_tree_lines):
            subprocess.check_call(["git", "show", commit])

def git_recursive(git_svn_command):
    def _recursive_git_svn_command(path="."):
        path = os.path.abspath(path)
        logger.info("Working in %s", path)
        def iter_git_folders(path):
            with ch(path):
                if os.path.exists(".git"):
                    yield os.path.abspath(path)
                for subpath in os.listdir(path):
                    for gitfolder in iter_git_folders(subpath):
                        yield gitfolder
        for gitpath in iter_git_folders(path):
            git_svn_command(gitpath)
    return _recursive_git_svn_command

# svn helpers

def svn_info():
    info = lsh(["svn", "info"]).decode("utf8")
    info_dict = {}
    for line in info.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            info_dict[key.strip()] = value.strip()
    return info_dict

def svn_externals():
    externals = lsh(["svn", "st"]).decode("utf8")
    seen = set()
    for line in externals.split("\n"):
        if line.strip() and line.startswith("X"):
            path = line.split()[1].strip()
            root = os.path.dirname(path)
            if root not in seen:
                seen.add(root)
            else:
                continue
            props = lsh(["svn", "propget", "svn:externals", root]).decode("utf8")
            for prop in props.split("\n"):
                if prop.strip():
                    yield root, prop.strip()

def extpath_join(root, uri):
    if uri.startswith("^"):
        return root + uri[1:]
    else:
        raise NotImplementedError

def normalize_externals(repo_root, externals):
    # Old syntax: third-party/sounds   http://svn.example.com/repos/sounds [UNSUPPORTED]
    # New syntax: -r148 ^/skinproj third-party/skins
    # peg syntax: ^/skinproj@148 third-party/skins
    for root, external in externals:
        parts = external.split()
        if len(parts) == 2:
            rev = None
            uri, path = parts
            if "@" in uri:
                uri, rev = uri.split("@")
        elif len(parts) == 3:
            rev, uri, path = parts()
            rev = rev.strip("-r")
        yield rev, extpath_join(repo_root, uri), os.path.normpath(os.path.join(root, path))

# Command line helpers

def check_svn(path):
    try:
        out = lsh(["svn", "info", path]).decode("utf8")
    except subprocess.CalledProcessError:
        raise argparse.ArgumentError("Invalid svn working copy!\nsvn info {0} returned:\n\n{1}".format(path, out))
    return path

def check_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentError("Invalid path {0:r}".format(path))

def git_svn_command(command_name):
    command = eval("git_svn_%s" % command_name)
    def run_git_svn_command():
        parser = argparse.ArgumentParser(description="Auto stashing git svn {0}".format(command_name))
        parser.add_argument("path", help="Point to an existing path", type=check_svn, default=".")
        parser.add_argument("-r", "--recursive", help="Recur in all git subfolders")
        parser.add_argument("-v", "--verbose", action='store_true')

        args, other_args = parser.parse_known_args()
        logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

        # normalize outputs
        with lang("C"):
            if not args.recursive:
                command(args.path)
            else:
                git_recursive(command)(args.path)
    return run_git_svn_command

run_dcommit = git_svn_command("dcommit")
run_rebase = git_svn_command("rebase")
run_outgoing = git_svn_command("outgoing")

def run():
    parser = argparse.ArgumentParser(description="git svn clone and follow svn:externals, \
                                                  all unknown arguments are forwarded \
                                                  (use -r HEAD for a shallow clone)")
    parser.add_argument("working_copy", help="Point to an existing svn checkout", type=check_svn)
    parser.add_argument("destination", help="Destination folder")
    parser.add_argument("-v", "--verbose", action='store_true')

    args, other_args = parser.parse_known_args()
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    # normalize svn output
    with lang("C"):
        externals = []
        with cd(args.working_copy):
            repo_info = svn_info()
            repo_root = repo_info["Repository Root"]
            for rev, uri, path in normalize_externals(repo_root, svn_externals()):
                externals += [(rev, uri, path)]

        repo_url = repo_info["URL"]
        commands = ["git", "svn", "clone"]
        commands += other_args
        commands += [repo_url, args.destination]
        logged_call(subprocess.call, logger.info)(commands)
        with cd(args.destination):
            for rev, uri, path in externals:
                commands = ["git", "svn", "clone"]
                commands += other_args
                commands += [uri, path]
                logged_call(subprocess.call, logger.info)(commands)
                if not [x for x in os.listdir(path) if x != ".git"]:
                    logger.warning("{0}Foder {path} is empty after clone!{1}".format(col.YELLOW, col.ENDC, **locals()))


if __name__ == "__main__":
    run()
