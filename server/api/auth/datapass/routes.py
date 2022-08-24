"""
Routes for authenticating using the 'Comptes DataPass' OpenID Connect server.

See: https://github.com/betagouv/api-auth
"""
import json
from textwrap import dedent

from fastapi import APIRouter
from pydantic import EmailStr
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from server.api.utils.urls import get_client_root_url
from server.application.auth.commands import CreateDataPassUser
from server.application.auth.queries import LoginDataPassUser
from server.config.di import resolve
from server.domain.auth.exceptions import LoginFailed
from server.domain.organizations.repositories import OrganizationRepository
from server.domain.organizations.types import Siret
from server.infrastructure.auth.datapass import DataPassOpenIDClient
from server.seedwork.application.messages import MessageBus

router = APIRouter(prefix="/datapass")


@router.get(
    "/login/",
    status_code=302,
    response_class=RedirectResponse,
    name="datapass_login",
    responses={
        302: {
            "description": dedent(
                """
                Successful Response

                The client is redirected to the Comptes DataPass authorization server.
                """
            )
        }
    },
)
async def login(request: Request) -> Response:
    """
    Trigger the OpenID Connect 'Authorization code' flow with Comptes DataPass.

    This should be called by the frontend client.
    """
    oauth = resolve(DataPassOpenIDClient)
    callback_uri = request.url_for("datapass_callback")
    return await oauth.authorize_redirect(request, callback_uri)


@router.get(
    "/callback/",
    status_code=307,
    name="datapass_callback",
    responses={
        307: {
            "description": dedent(
                """
                Successful Response

                The `Location` header may be one of 3 cases, depending on the
                number of matching organizations.

                ### 1 matching organization

                Redirected URL: `<client_root_url>/auth/datapass/login`

                If the user's DataPass organizations match with exactly 1 known
                organization.

                In this case, a user account is created and user information is sent
                back as query parameters for the frontend to consume.

                #### Redirected URL query parameters

                * `organization_siret`: `string($siret)`
                * `email`: `string($email)`
                * `role`: `UserRole`
                * `api_token`: `string`

                ### 0 matching organization

                Redirected URL: `<client_root_url>/auth/datapass/create-organization`

                If the user's DataPass organizations don't match with any known
                organization.

                The user should be prompted to create one.

                ### 2+ matching organizations

                Redirected URL: `<client_root_url>/auth/datapass/pick-organization`

                If the user's DataPass organizations match with 2 or more known
                organizations.

                The user should be prompted to pick one of those.

                #### Redirected URL query parameters

                * `organizations`: a URL-encoded JSON object containing a list
                  of organizations represented as:

                    ```json
                    {
                        "siret": "string($siret)",
                        "name": "string"
                    }
                    ```
                """
            )
        }
    },
)
async def callback(request: Request) -> Response:
    """
    OpenID Connect callback route for 'Comptes DataPass'.

    Called by 'Comptes DataPass' upon successful login or registration.
    """
    # NOTE: For each deployed environment, one copy of this callback has been registered
    # on the appropriate 'Comptes DataPass' instance (staging or prod).

    bus = resolve(MessageBus)
    oauth = resolve(DataPassOpenIDClient)
    organization_repository = resolve(OrganizationRepository)

    userinfo = await oauth.authorize_userinfo(request)

    email = EmailStr(userinfo["email"])

    try:
        account = await bus.execute(LoginDataPassUser(email=email))
    except LoginFailed:
        their_datapass_organizations = userinfo["organizations"]

        sirets_here = await organization_repository.get_siret_set()

        their_organizations_here = [
            organization
            for organization in their_datapass_organizations
            if organization["siret"] in sirets_here
        ]

        if len(their_organizations_here) == 0:
            # None of the user's organizations have been registered in our system yet.
            url = get_client_root_url()
            url = url.replace(path="/auth/datapass/create-organization")
            return RedirectResponse(url, status_code=307)

        if len(their_organizations_here) > 1:
            # More than one of the user's organizations is registered in our system,
            # we need the user to pick one.
            choices = [
                {"siret": org["siret"], "name": org["label"]}
                for org in their_organizations_here
            ]
            url = get_client_root_url()
            url = url.replace(path="/auth/datapass/pick-organization")
            url = url.include_query_params(organizations=json.dumps(choices))
            return RedirectResponse(url, status_code=307)

        organization_siret = Siret(their_organizations_here[0]["siret"])

        await bus.execute(
            CreateDataPassUser(
                organization_siret=organization_siret,
                email=email,
            )
        )

        account = await bus.execute(LoginDataPassUser(email=email))

    url = get_client_root_url()
    url = url.replace(path="/auth/datapass/login")
    url = url.include_query_params(
        # These will be grabbed by the frontend and stored in its localStorage as the
        # currently authenticated user.
        # Protected against MITM attacks as long as we serve over HTTPS.
        organization_siret=account.organization_siret,
        email=account.email,
        role=account.role.value,
        api_token=account.api_token,
    )

    return RedirectResponse(url, status_code=307)