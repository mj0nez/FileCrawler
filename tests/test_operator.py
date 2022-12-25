from fileswitch.operator import move_file
from fs import open_fs
from pathlib import Path


def test_move_between_2_fs():
    fs_src = open_fs("./tests/data/source")
    fs_src.writetext("README.md", "Tetris clone")
    fs_trgt = open_fs("./tests/data/target")
    move_file(fs_src, "README.md", fs_trgt, "README.md", True)

    fs_trgt.remove("README.md")


def test_move_between_same_fs():
    fs_data = open_fs("./tests/data")
    fs_data.writetext("target/README.md", "Tetris clone")

    move_file(fs_data, "target/README.md", fs_data, "source/README.md", True)
    
    # ?!?!
    # the test fails if the target path does not exists 

    # fs_data.remove("./source/README.md")
