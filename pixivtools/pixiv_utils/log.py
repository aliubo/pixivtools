from datetime import datetime
from pathlib import Path


class PixivLog():
    def __init__(self, file_path: Path):
        self._file = file_path.open('a+', encoding="utf-8")

    def __del__(self):
        self._file.close()

    def log(self, lvl, msg, *args, **kwargs):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record_text = f'[{time}][{lvl}]: {msg} {args} {kwargs}'
        print(record_text)
        if self._file.writable():
            self._file.write(record_text + '\n')


    def info(self, msg, *args, **kwargs):
        self.log('Info', msg, *args, **kwargs)


    def warning(self, msg, *args, **kwargs):
        self.log('Warning', msg, *args, **kwargs)


    def error(self, msg, *args, **kwargs):
        self.log('Error', msg, *args, **kwargs)
