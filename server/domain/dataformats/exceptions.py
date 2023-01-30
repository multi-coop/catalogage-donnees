from server.domain.dataformats.entities import DataFormat


class DataFormatAlreadyExists(Exception):
    def __init__(self, dataformat: DataFormat) -> None:
        super().__init__()
        self.dataformat = dataformat
