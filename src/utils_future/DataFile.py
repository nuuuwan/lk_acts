import os
from functools import cached_property

from utils import JSONFile, Log

from utils_future.FileFuture import FileFuture

log = Log("DataFile")


class DataFile(FileFuture):
    def __init__(self, get_path, get_data):
        super().__init__(get_path())
        self.get_path = get_path
        self.get_data = get_data

    @cached_property
    def path_fail(self):
        return self.path + ".fail"

    def __get_data_hot__(self):
        data = self.get_data()
        if data is not None:
            self.write(data)
            return data
        JSONFile(self.path_fail).write("")
        return None

    def io_class(self):
        return JSONFile if self.path.endswith(".json") else FileFuture

    def read(self):
        content = self.io_class()(self.path).read()
        return content

    @staticmethod
    def get_write_message(content):
        if isinstance(content, list):
            return f"{len(content):,} items"
        if isinstance(content, str):
            return f"{len(content):,} chars"
        raise ValueError(f"Unsupported data type: {type(content).__name__}")

    def write(self, content):
        self.io_class()(self.path).write(content)
        log.info(
            f"Wrote {self.path}"
            + f" ({self.get_write_message(content)}, {self.size_humanized})"
        )

    @cached_property
    def data(self):
        if os.path.exists(self.path):
            return self.read()

        if os.path.exists(self.path_fail):
            return None

        return self.__get_data_hot__()
