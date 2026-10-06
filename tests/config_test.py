import pytest
from mazegen import Config
from tests import TmpFile


VALID_CONTENT = """
# Default configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
""".strip()


def test_openfilenotfound() -> None:
    with pytest.raises(Config.FileError, match="not found"):
        Config.open("missing_config.txt")


def test_openfilepermissions() -> None:
    with TmpFile("", False) as path:
        with pytest.raises(Config.FileError, match="Unauthorized"):
            Config.open(path)


def test_syntaxerror() -> None:
    ...


def test_valid() -> None:
    with TmpFile(VALID_CONTENT) as path:
        Config.open(path)
