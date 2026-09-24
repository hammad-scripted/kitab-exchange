import hmac
import os

from fastapi import Header, HTTPException

API_KEY = os.getenv("KITAB_EXCHANGE_API_KEY")


def verify_api_key(api_key: str = Header()):
    if not API_KEY:
        raise HTTPException(status_code=503, detail="API key is not configured")
    if not hmac.compare_digest(api_key.encode(), API_KEY.encode()):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key
