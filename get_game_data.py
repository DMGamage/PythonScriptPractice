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


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)


def get_name_from_paths(path, to_strip):
    new_names = []
    for path in path:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names


def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }
    with open(path, "w") as f:
        json.dump(data, f)


def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    source_target = os.path.join(cwd, target)

    game_paths = find_all_paths(source)
    new_game_dir = get_name_from_paths(game_paths, "game")

    create_dir(source_target)

    for src, dest in zip(game_paths, new_game_dir):
        dest_path = os.path.join(source_target, dest)
        copy_and_overwrite(src, dest_path)

    json_path = os.path.join(source_target, "metadata.json")
    make_json_metadata_file(json_path, new_game_dir)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception(f"You must have pass Source and Target directory")

    source, target = args[1:]
    main(source, target)
