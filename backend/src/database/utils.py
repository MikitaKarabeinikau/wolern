# backend/src/database/utils.py
from fastapi import HTTPException
from clerk_backend_api import Clerk, AuthenticateRequestOptions
import os
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)

def _get_env_vars():
    CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
    JWK_KEY = os.getenv("JWK_KEY")
    return CLERK_SECRET_KEY, JWK_KEY

def _get_clerk_sdk():
    CLERK_SECRET_KEY, JWK_KEY = _get_env_vars()
    if not CLERK_SECRET_KEY:
        raise ValueError("CLERK_SECRET_KEY environment variable is not set.")
    if not JWK_KEY:
        raise ValueError("JWK_KEY environment variable is not set.")
    return Clerk(bearer_auth=CLERK_SECRET_KEY), JWK_KEY

def authenticate_and_get_user_details(request):
    # Ensure Authorization header exists first
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        clerk_sdk, jwk_key = _get_clerk_sdk()
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173", "http://localhost:5172"],
                jwt_key=jwk_key,
            ),
        )
        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Invailid token")

        user_id = request_state.payload.get("sub")
        print("Authenticated user ID:", user_id)
        return {
            "user_id": user_id,
            "email": request_state.payload.get("email"),
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Clerk SDK authentication crash: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed: Token processing error.")
