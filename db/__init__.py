from settings.config import DB_CONFIG

TORTOISE_ORM = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.asyncpg",    # 引擎是asyncpg
                "credentials": DB_CONFIG,
            }
        },
        "apps": {
            "models": {
                "models": ['db.table'],
                "default_connection": "default",
            }
        },
        "use_tz": False,
        "timezone":  "Asia/Shanghai",
}
