import os
import sys
import json
import shutil
from subprocess import PIPE, run

GAME_DIR_PATTERN = "game"


def find_all_paths(source):
    game_paths = []

    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)

        break
    return game_paths


def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    source_target = os.path.join(cwd, target)

    game_paths = find_all_paths(source)
    print(game_paths)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception(f"You must have pass Source and Target directory")

    source, target = args[1:]
    main(source, target)
