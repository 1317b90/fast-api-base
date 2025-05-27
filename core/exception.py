from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

class BusinessException(Exception):
    def __init__(self, code: int = 4001, message: str = "业务异常"):
        self.code = code
        self.message = message

def register_exceptions(app: FastAPI):
    @app.exception_handler(BusinessException)
    async def business_handler(request: Request, exc: BusinessException):
        return JSONResponse(
            status_code=200,
            content={"code": exc.code, "message": exc.message, "data": None}
        )

    @app.exception_handler(Exception)
    async def global_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"code": 5000, "message": "系统错误：" + str(exc), "data": None}
        )