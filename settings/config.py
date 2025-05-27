DB_CONFIG={
    "host": "127.0.0.1",
    "port": 3306,
    "user": "test",
    "password": "123456",
    "database": "test",
    "maxsize": 20,  # 最大连接数
    "ssl": False
}

#TODO TOKEN配置
SECRET_KEY = "47A405D9F2C0A401744002C78E0CD576"
ACCESS_TOKEN_EXPIRE_MINUTES=480 # Token时效
EXCLUDE_PATHS=["/login", "/docs", "/redoc", "/openapi.json","/login/swagger"] # 不需要验证的路径