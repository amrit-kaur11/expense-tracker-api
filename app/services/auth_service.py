from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationException, EntityAlreadyExistsException
from app.core.security import create_access_token, decode_access_token, get_password_hash, verify_password
from app.models.user import User
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.token import Token
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.token_repo = TokenRepository(db)

    def register_user(self, user_in: UserCreate) -> User:
        """Register a new user account."""
        existing_user = self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise EntityAlreadyExistsException("A user with this email already exists")

        hashed_password = get_password_hash(user_in.password)
        user = self.user_repo.create_user(
            name=user_in.name,
            email=user_in.email,
            password_hash=hashed_password
        )
        return user

    def authenticate_user(self, email: str, password: str) -> Token:
        """Authenticate user credentials and generate JWT access token."""
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise AuthenticationException("Invalid email or password")

        access_token = create_access_token(subject=user.id)
        return Token(access_token=access_token, token_type="bearer")

    def logout_user(self, token: str) -> None:
        """Revoke JWT access token by adding it to the blacklist."""
        payload = decode_access_token(token)
        if not payload:
            raise AuthenticationException("Invalid token")

        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        else:
            expires_at = datetime.now(timezone.utc)

        self.token_repo.blacklist_token(token, expires_at)

    def get_current_user(self, token: str) -> User:
        """Decode and validate access token, ensuring token is active and not blacklisted."""
        if self.token_repo.is_blacklisted(token):
            raise AuthenticationException("Token has been revoked/logged out")

        payload = decode_access_token(token)
        if not payload:
            raise AuthenticationException("Invalid or expired token")

        user_id_str = payload.get("sub")
        if not user_id_str:
            raise AuthenticationException("Token subject missing")

        try:
            user_id = int(user_id_str)
        except ValueError:
            raise AuthenticationException("Invalid user ID in token")

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise AuthenticationException("User account not found")

        return user
