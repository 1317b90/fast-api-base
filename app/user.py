from db.table import User, User_Pydantic, UserIn_Pydantic
from fastapi import APIRouter, HTTPException, Body

router = APIRouter()

@router.post("/user", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic = Body(...)):
    await user.save()
    return user


@router.get("/user/{user_id}", response_model=User_Pydantic)
async def get_user(user_id: int):
    user = await User.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

