from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

def SuccessResponse(message: str, data = None):
    return {"code": 200, "message": message, "data": data}

class ExceptionResponse(Exception):
    def __init__(self, code: int = 400, message: str = "业务异常",data= None):
        self.code = code
        self.message = message
        self.data = data

def register_exceptions(app: FastAPI):
    @app.exception_handler(ExceptionResponse)
    async def business_handler(request: Request, exc: ExceptionResponse):
        return JSONResponse(
            status_code=exc.code,
            content={"code": exc.code, "message": exc.message, "data": exc.data}
        )

    @app.exception_handler(Exception)
    async def global_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"code": 500, "message": "系统错误：" + str(exc), "data": None}
        )