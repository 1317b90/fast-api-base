from db.table import User, UserIn_Pydantic
from fastapi import APIRouter, Body
from core.response import SuccessResponse, ExceptionResponse
from tortoise.exceptions import DoesNotExist
from fastapi import APIRouter
from app.auth import get_password_hash

router = APIRouter(tags=["用户"])

@router.post("/user", summary="创建用户")
async def _(user: UserIn_Pydantic = Body(...)):
    # 检查用户是否存在
    user_exists = await User.filter(username=user.username).first()
    if user_exists:
        raise ExceptionResponse(code=400, message="用户已存在")
    
    # 创建用户数据字典并加密密码
    user_data = user.dict()
    user_data["password"] = get_password_hash(user_data["password"])
    
    # 创建新用户
    new_user = await User.create(**user_data)
    return SuccessResponse(message="用户创建成功", data=new_user)

@router.get("/user/{user_id}", summary="获取用户")
async def _(user_id: int):
    try:
        user = await User.get(id=user_id)
        return SuccessResponse(message="获取用户成功", data=user)
    except DoesNotExist:
        raise ExceptionResponse(code=404, message="用户不存在")

@router.get("/users", summary="获取用户列表")
async def _(skip: int = 0, limit: int = 10):
    users = await User.all().offset(skip).limit(limit)
    return SuccessResponse(message="获取用户列表成功", data=users)

@router.put("/user/{user_id}",summary="更新用户")
async def _(user_id: int, user: UserIn_Pydantic = Body(...)):
    try:
        existing_user = await User.get(id=user_id)
        
        # 检查name是否被其他用户使用
        if user.username != existing_user.username:
            username_exists = await User.filter(username=user.username).first()
            if username_exists:
                raise ExceptionResponse(code=400, message="用户名已被其他用户使用")
        
        # 更新用户信息
        await existing_user.update_from_dict(user.dict()).save()
        return SuccessResponse(message="用户更新成功", data=existing_user)
    except DoesNotExist:
        raise ExceptionResponse(code=404, message="用户不存在")

@router.delete("/user/{user_id}",summary="删除用户")
async def _(user_id: int):
    try:
        user = await User.get(id=user_id)
        await user.delete()
        return SuccessResponse(message="用户删除成功")
    except DoesNotExist:
        raise ExceptionResponse(code=404, message="用户不存在")


