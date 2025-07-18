from fastapi import APIRouter
from config.users import auth_backend, fastapi_users
from schemas.user import UserRead, UserCreate, UserUpdate


auth_router = APIRouter(prefix="/auth", tags=["auth"])

# JWT Authentication routes
auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

# Registration routes
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)

# Password reset routes
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["auth"],
)

# Email verification routes
auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    tags=["auth"],
)

# Authenticated user management routes
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
