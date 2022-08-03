from server.application.auth.commands import (
    ChangePassword,
    CreatePasswordUser,
    DeletePasswordUser,
)
from server.application.auth.handlers import (
    change_password,
    create_password_user,
    delete_password_user,
    get_account_by_api_token,
    get_account_by_email,
    login_password_user,
)
from server.application.auth.queries import (
    GetAccountByAPIToken,
    GetAccountByEmail,
    LoginPasswordUser,
)
from server.seedwork.application.modules import Module


class AuthModule(Module):
    command_handlers = {
        CreatePasswordUser: create_password_user,
        DeletePasswordUser: delete_password_user,
        ChangePassword: change_password,
    }

    query_handlers = {
        LoginPasswordUser: login_password_user,
        GetAccountByEmail: get_account_by_email,
        GetAccountByAPIToken: get_account_by_api_token,
    }
