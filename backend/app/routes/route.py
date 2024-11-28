from fastapi import APIRouter, HTTPException, Depends
from app.models.model import User
from app.config.database import collection_name
from app.auth.jwt import (
    create_access_token,
    verify_password,
    get_password_hash,
    get_current_user,
)
from app.schemas.schema import users_serializer, user_serializer
from bson import ObjectId

user_router = APIRouter()

# Login Endpoint - Generates Access Token
@user_router.post("/login")
async def login(username: str, password: str):
    user = collection_name.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


# Register a New User
@user_router.post("/")
async def create_user(user: User):
    user.password = get_password_hash(user.password)
    _id = collection_name.insert_one(dict(user))
    return users_serializer(collection_name.find({"_id": _id.inserted_id}))


# Forgot Password - Verify Email
@user_router.post("/forgot-password")
async def forgot_password(email: str):
    user = collection_name.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User with this email does not exist")
    return {"message": "Email verified. Please set a new password."}


# Forgot Password - Reset Password
@user_router.post("/reset-password")
async def reset_password(email: str, new_password: str, confirm_password: str):
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = get_password_hash(new_password)
    user = collection_name.find_one_and_update(
        {"email": email},
        {"$set": {"password": hashed_password}},
    )
    if not user:
        raise HTTPException(status_code=404, detail="User with this email does not exist")
    return {"message": "Password updated successfully"}


# Protected Endpoint: Get Current User Details
@user_router.get("/user")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"], "email": current_user["email"]}


# Protected Endpoint: Retrieve All Users
@user_router.get("/")
async def get_users(current_user: dict = Depends(get_current_user)):
    users = users_serializer(collection_name.find())
    return users


# Protected Endpoint: Update User by ID
@user_router.put("/{id}")
async def update_user(id: str, user: User, current_user: dict = Depends(get_current_user)):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
    return users_serializer(collection_name.find({"_id": ObjectId(id)}))


# Protected Endpoint: Delete User by ID
@user_router.delete("/{id}")
async def delete_user(id: str, current_user: dict = Depends(get_current_user)):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "ok"}
