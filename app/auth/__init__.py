import jwt
import datetime
import secrets
import hashlib
from datetime import timezone
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from typing import Optional
from settings.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, EXCLUDE_PATHS
from core.response import ExceptionResponse
from db.table import User

def generate_salt() -> str:
    """生成随机盐值"""
    return secrets.token_hex(16)

def hash_password_with_salt(password: str, salt: str) -> str:
    """使用盐值对密码进行哈希"""
    # 使用 SHA-256 算法
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password_with_salt(password: str, salt: str, hashed_password: str) -> bool:
    """验证密码"""
    return hash_password_with_salt(password, salt) == hashed_password

# 自定义OAuth2PasswordBearer类，解决登录接口和文档问题
class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str):
        super().__init__(
            tokenUrl=tokenUrl,
            scheme_name=None,
            scopes=None,
            description=None,
            auto_error=True
        )

    async def __call__(self, request: Request) -> Optional[str]:
        path: str = request.url.path
        # 对于不需要验证的路径，直接返回空字符串
        if any(path.startswith(excluded) for excluded in EXCLUDE_PATHS):
            return ""
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise ExceptionResponse(code=405, message="请求未携带token")
            else:
                return None
        
        # 直接在这里验证token
        try:
            payload = jwt.decode(
                param,
                SECRET_KEY,
                algorithms=["HS256"],
            )
            username = payload.get("username")
            if username is None:
                raise ExceptionResponse(code=405, message="无效的token内容")
            else:
                user = await User.get(username=username)
                if user is None:
                    raise ExceptionResponse(code=405, message="用户不存在")
                else:
                    return username
        except jwt.ExpiredSignatureError:
            raise ExceptionResponse(code=406, message="token已过期")
        except jwt.InvalidTokenError:
            raise ExceptionResponse(code=405, message="token无效")

# 使用自定义的OAuth2PasswordBearer
oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl="login/swagger")

# 创建token
def create_token(data:dict):
    to_encode = data.copy()
    to_encode.update({"exp":datetime.datetime.now(timezone.utc)+datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt

