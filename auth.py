# backend/langchain_app/api/auth.py

import jwt
import datetime
from fastapi import HTTPException, Header

# --- JWT Config ---
SECRET_KEY = "your_secret_key"  # Replace with strong secret
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 3000000

# --- Generate JWT ---
def create_access_token(collection_name: str) -> str:
    if collection_name != "manuals":
        raise ValueError("Token can only be generated for 'manuals' collection.")
    
    payload = {
        "collection": collection_name,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# --- Verify JWT (for FastAPI auth protection) ---
def verify_token(authorization: str = Header(..., alias="Authorization")) -> dict:
    try:
        # Extract token from "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization scheme.")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

# generate_token.py


if __name__ == "__main__":
    try:
        token = create_access_token("manuals")
        print("Generated JWT Token:\n")
        print(token)
    except ValueError as e:
        print(f"Error generating token: {e}")
