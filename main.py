from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from core.response import register_exceptions
from app.auth import user
from db import TORTOISE_ORM
from app.auth import oauth2_scheme,login


app = FastAPI(
    title="FastAPIBase",
    dependencies=[Depends(oauth2_scheme)],  # 添加全局依赖，让所有接口都需要验证
)
register_exceptions(app)

# 添加路由
app.include_router(user.router)
app.include_router(login.router)

# 解决跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True, # 自动生成数据库表
    add_exception_handlers=False,# 数据库调试信息
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
