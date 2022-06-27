#!/usr/bin/env python3
import re
import sys
import os
import shutil
import subprocess
from typing import List
from src.utils import *

def main(args: List[str] = sys.argv[1:]):
    # If no clang-tidy-diff binary, exit with 1.
    clang_tidy_diff_bin = 'clang-tidy-diff'
    if shutil.which(clang_tidy_diff_bin) is None:
        exit_with("Cannot find clang-tidy-diff binary")
    # If no build directory, exit with 1.
    dir_path = parse_dir_path(args)
    if not dir_path.exists():
        exit_with("Cannot find the build directory for compile_commands: " + str(dir_path.resolve()))
    if not (dir_path / 'compile_commands.json').exists():
        exit_with("Cannot find compile_commands.json in the build directory: " + str(dir_path.resolve()))

    # from_ref = PRE_COMMENT_FROM_REF? PRE_COMMIT_FROM_REF : origin/main
    from_ref = os.environ.get('PRE_COMMIT_FROM_REF', 'origin/main')
    # output = git diff --no-prefix from_ref -U0 | clang-tidy-diff <args>
    diff = subprocess.Popen(args=['git', 'diff', '--no-prefix', from_ref, '-U0'], stdout=subprocess.PIPE)
    clang_tidy_command = [clang_tidy_diff_bin, *args]
    output = subprocess.check_output(args=clang_tidy_command, stdin=diff.stdout, stderr=subprocess.STDOUT, text=True)
    diff.wait()
    # Strip useless messages.
    output = re.sub(r"\s*No relevant changes found.\s*", "", output)
    output = re.sub(r"\s*[\d]+ warnings generated\.\s*", "", output)
    # If any error exists, then exit with 1.
    if re.search(r": error:", output):
        exit_with(output, 1)

if __name__ == "__main__":
    main()
