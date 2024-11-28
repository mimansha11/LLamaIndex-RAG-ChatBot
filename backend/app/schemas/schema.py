def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "username": user["username"],
        "password": user["password"],
        "email": user["email"],
        "gender": user["gender"],
        
    }

def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]