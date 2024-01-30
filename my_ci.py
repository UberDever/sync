#!/usr/bin/python3

import subprocess
import sys
import os
import io

COMMANDS_MARK = "# " + "The Commands"


def ENV(name) -> str:
    return os.environ[name]


def generate_usage(filepath) -> str:
    command_lines = []
    reading_commands = False
    with open(filepath, 'r') as file:
        for line in file.readlines():
            if COMMANDS_MARK in line:
                reading_commands = True
            elif '__name__ == "__main__"' in line:
                reading_commands = False
            if reading_commands:
                if line.startswith('def'):
                    command_lines.append(line)
    return "\n".join(command_lines)


def run_command_with_check(cmd, cwd) -> str:
    result = subprocess.run(cmd, encoding='UTF-8', cwd=cwd,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        print(f"Failed with returncode {result.returncode}")
        print(result.stderr)
        exit(-1)
    output = result.stdout
    return str(output)


def get_changed_files(cwd) -> str:
    git_cmd = ['git', 'diff-tree', '--no-commit-id',
               '--name-only', '-r', 'HEAD']
    changed = run_command_with_check(git_cmd, cwd)
    paths = changed.split('\n')
    return [p for p in paths if len(p)]


def run_clang_tidy_check(paths, cwd) -> str:
    def clang_tidy_cmd(path): return [os.path.join(ENV('core_dir'),
                                                   "scripts",
                                                   "clang-tidy",
                                                   "clang_tidy_check.py",
                                                   ),
                                      '--filename-filter=' + path,
                                      ENV('core_dir'),
                                      os.path.join(ENV('arkc_dir'), 'build'),
                                      ]

    for path in paths:
        cmd = clang_tidy_cmd(path)
        print(f"Running {cmd}")
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
            yield line

# The Commands


def clang_tidy():  # get cwd and run clang-tidy check on the files that changed by git diff-tree command
    print(f"Looking for git in {os.getcwd()}")
    to_check = get_changed_files(os.getcwd())
    for line in run_clang_tidy_check(to_check, os.getcwd()):
        print(line)


def some_command(): pass


if __name__ == "__main__":
    usage = generate_usage(os.path.abspath(__file__))
    if len(sys.argv) == 1:
        print(usage)
        exit(0)
    cmd = sys.argv[1]
    args = ['"' + arg + '"' for arg in sys.argv[2:]]
    eval(cmd + "({0})".format(",".join(args)))
