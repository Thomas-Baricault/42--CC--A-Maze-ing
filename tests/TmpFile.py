from os import chmod, fdopen, O_CREAT, O_TRUNC, O_WRONLY, open, remove
from typing import Any, Tuple


class TmpFile:
    def __init__(self, content: str, permissions: bool = True) -> None:
        self._path = "tests/tmp"
        self._content = content
        self._permissions = permissions

    def __enter__(self) -> str:
        fd = open(self._path, O_CREAT | O_TRUNC | O_WRONLY)
        with fdopen(fd, "w") as file:
            file.write(self._content)
        chmod(self._path, 0o666 if self._permissions else 0)
        return self._path

    def __exit__(self, *_: Tuple[Any, ...]) -> None:
        chmod(self._path, 0o666)
        remove(self._path)
