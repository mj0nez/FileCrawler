# from fileswitch.operator import move_file
from fs import open_fs
from pathlib import Path
from fs.move import move_file


def test_move_between_2_fs():
    fs_src = open_fs("./tests/data/source")
    fs_src.writetext("README.md", "Tetris clone")
    fs_trgt = open_fs("./tests/data/target")
    move_file(fs_src, "README.md", fs_trgt, "README.md", True)

    fs_trgt.remove("README.md")


def test_move_between_same_fs():
    fs_data = open_fs("tests/data")
    fs_data.writetext("target/README.md", "Tetris clone")

    move_file(
        src_fs=fs_data,
        src_path="target/README.md",
        dst_fs=fs_data,
        dst_path="source/README.md",
        preserve_time=True,
    )

    fs_data.remove("source/README.md")
