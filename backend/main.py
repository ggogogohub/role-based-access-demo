from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Simulated users with roles
users_db = {
    "admin_token": {"username": "admin", "role": "admin"},
    "user_token": {"username": "user", "role": "user"}
}

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = users_db.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.get("/data")
def get_data(current_user: dict = Depends(get_current_user)):
    if current_user["role"] == "admin":
        return {"message": f"Hello {current_user['username']}, you have full access."}
    elif current_user["role"] == "user":
        return {"message": f"Hello {current_user['username']}, you have limited access."}
    else:
        raise HTTPException(status_code=403, detail="Access forbidden")
