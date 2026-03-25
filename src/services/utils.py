from fastapi_users.password import PasswordHelper

password_helper = PasswordHelper()


def get_hashed_password(password: str) -> str:
    return password_helper.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    verified, _ = password_helper.verify_and_update(password, hashed_pass)
    return verified
