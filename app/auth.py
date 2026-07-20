import secrets

from fastapi import Header, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .config import settings

security = HTTPBasic()


def verify_upload_token(
    authorization: str = Header(default="")
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )

    token = authorization[7:]

    if not secrets.compare_digest(
        token,
        settings.UPLOAD_TOKEN,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def verify_basic(credentials: HTTPBasicCredentials):

    correct_user = secrets.compare_digest(
        credentials.username,
        settings.WEB_USERNAME,
    )

    correct_pass = secrets.compare_digest(
        credentials.password,
        settings.WEB_PASSWORD,
    )

    if not (correct_user and correct_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username