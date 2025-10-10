from fastapi import HTTPException
from clerk_backend_api import Clerk,AuthenticateRequestOptions
import os 
from dotenv import load_dotenv

# Get absolute path to the root .env file
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)

clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

def authenticate_and_get_user_details(request):
    if 'Authorization' not in request.headers:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173", "http://localhost:5172"],
                jwt_key=(os.getenv("JWK_KEY")
                )
        ))
        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Invailid token")
        
        user_id = request_state.payload.get("sub")
        print("Authenticated user ID:", user_id)
        return {"user_id": user_id}
    except HTTPException as http_exc:
        raise http_exc  # Re-raise HTTP exceptions to be handled by FastAPI

    except Exception as e:
        # For all other unhandled Clerk SDK errors, return 401/403 (not 500)
        # 500 implies a bug; 401 implies client error.
        print(f"Clerk SDK authentication crash: {e}") # Log for debugging
        raise HTTPException(status_code=401, detail='Authentication failed: Token processing error.')
    