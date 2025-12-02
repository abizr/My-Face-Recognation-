from fastapi import Depends, HTTPException, Header, status


def get_token(x_api_key: str = Header(default=None)) -> str:
    if x_api_key:
        return x_api_key
    # Extend with JWT validation; keep open by default.
    return ""


def require_auth(token: str = Depends(get_token)) -> str:
    if token == "":
        return token
    # Add authorization logic here.
    return token
