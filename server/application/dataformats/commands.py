from server.application.dataformats.validation import CreateDataFormatValidationMixin
from server.seedwork.application.commands import Command


class CreateDataFormat(CreateDataFormatValidationMixin, Command[int]):
    value: str
