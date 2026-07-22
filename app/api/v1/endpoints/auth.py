from fastapi import APIRouter, Depends, Header, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationException
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import LogoutResponse, Token
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Dependency helper to validate JWT token and retrieve the current authenticated user."""
    if not token:
        raise AuthenticationException("Not authenticated")
    auth_service = AuthService(db)
    return auth_service.get_current_user(token)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Register new user")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account."""
    auth_service = AuthService(db)
    return auth_service.register_user(user_in)


@router.post("/login", response_model=Token, summary="User login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user credentials and return JWT access token."""
    auth_service = AuthService(db)
    return auth_service.authenticate_user(email=credentials.email, password=credentials.password)


@router.post("/logout", response_model=LogoutResponse, summary="User logout (Revoke token)")
def logout(
    token: str = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout authenticated user by blacklisting current JWT access token."""
    auth_service = AuthService(db)
    auth_service.logout_user(token)
    return LogoutResponse()


@router.get("/me", response_model=UserResponse, summary="Get current user profile")
def read_user_me(current_user: User = Depends(get_current_user)):
    """Fetch profile information for the authenticated user."""
    return current_user
