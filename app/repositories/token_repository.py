from datetime import datetime
from sqlalchemy.orm import Session

from app.models.blacklist import TokenBlacklist
from app.repositories.base import BaseRepository


class TokenRepository(BaseRepository[TokenBlacklist]):
    def __init__(self, db: Session):
        super().__init__(TokenBlacklist, db)

    def blacklist_token(self, token: str, expires_at: datetime) -> TokenBlacklist:
        """Add JWT access token to blacklist upon logout."""
        blacklisted = TokenBlacklist(token=token, expires_at=expires_at)
        return self.create(blacklisted)

    def is_blacklisted(self, token: str) -> bool:
        """Check if JWT access token has been revoked."""
        record = self.db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first()
        return record is not None
