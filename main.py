from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from core.exception import register_exceptions
from app import user
from db import TORTOISE_ORM

app = FastAPI(
    title="数据分析接口",
)
register_exceptions(app)

# 添加路由
app.include_router(user.router)

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
