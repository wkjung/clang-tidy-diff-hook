#!/usr/bin/env python3
import subprocess
from typing import List

from src.utils import *

def main(args: List[str] = sys.argv[1:]):
    path = parse_dir_path(args)
    cmd = ["compdb", "-p", path, "list"]
    new_compile_commands = subprocess.run(args=cmd, stdout=subprocess.PIPE).stdout
    (path / "compile_commands.json").write_bytes(new_compile_commands)

if __name__ == "__main__":
    main()
