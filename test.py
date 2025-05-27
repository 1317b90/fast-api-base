from app.auth import hash_password_with_salt

print(hash_password_with_salt("123456", "123456"))
