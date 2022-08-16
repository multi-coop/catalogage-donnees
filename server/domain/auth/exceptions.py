from ..common.exceptions import AlreadyExists, DoesNotExist


class AccountDoesNotExist(DoesNotExist):
    entity_name = "Account"


class EmailAlreadyExists(AlreadyExists):
    entity_name = "Email"


class DataPassUserAlreadyExists(AlreadyExists):
    entity_name = "DataPassUser"


class LoginFailed(Exception):
    pass
