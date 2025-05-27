from db.table import User
from fastapi import APIRouter, Body
from core.response import SuccessResponse, ExceptionResponse
from tortoise.exceptions import DoesNotExist
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_token, verify_password

router = APIRouter(tags=["登录"])

# 用于用户登录接口
@router.post("/login",summary="用户登录")
async def _(username:str=Body(...),password:str=Body(...)):
    try:
        # 从数据库获取用户信息
        user = await User.get(username=username)
        # 验证密码
        if not verify_password(password, user.password):
            raise ExceptionResponse(code=400, message="用户名或密码错误")
        # 创建访问令牌
        access_token = create_token({"username": user.username, "user_id": user.id})
        return SuccessResponse(message="登录成功",data={"token": access_token,"isAdmin":user.isAdmin})
    except DoesNotExist:
        raise ExceptionResponse(code=400, message="用户名或密码错误")

# 用于swagger的登录接口
@router.post("/login/swagger",summary="swagger登录")
async def _(user_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # 从数据库获取用户信息
        user = await User.get(username=user_data.username)
        # 验证密码
        if not verify_password(user_data.password, user.password):
            raise ExceptionResponse(code=400, message="用户名或密码错误")
        # 创建访问令牌
        access_token = create_token({"username": user.username, "user_id": user.id})

        # 返回符合Swagger的OAuth2规范的响应（必须此格式）
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except DoesNotExist:
        raise ExceptionResponse(code=400, message="用户名或密码错误")