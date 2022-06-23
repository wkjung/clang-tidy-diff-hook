#!/usr/bin/env python3
import sys
from pathlib import Path

def exit_with(msg, exit_code = 1):
    print(msg, file = sys.stderr)
    sys.exit(exit_code)

def parse_dir_path(args):
    if not '-path' in args:
        exit_with("No -path <build-dir> argument passed.", 1)
    path_idx = args.index('-path') + 1
    dir_path = args[path_idx]
    return Path(dir_path)

