from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)


password = "TestPassword123!"

hashed = hash_password(password)

print("Hash:")
print(hashed)

print("Correct password:", verify_password(password, hashed))
print("Wrong password:", verify_password("WrongPassword", hashed))


token = create_access_token(
    user_id=1,
    role="viewer",
)

print("JWT created successfully")
print(token)