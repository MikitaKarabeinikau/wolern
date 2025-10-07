from fastapi import HTTPException
from clerk_backend_api import Clerk,AuthenticateRequestOptions
import os 
from dotenv import load_dotenv

# Get absolute path to the root .env file
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)

clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

def authenticate_and_get_user_details(request):
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    