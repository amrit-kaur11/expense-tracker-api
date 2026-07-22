from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Fetch a single record by primary key id."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, limit: int = 100, offset: int = 0) -> List[ModelType]:
        """Fetch records with limit and offset pagination."""
        return self.db.query(self.model).offset(offset).limit(limit).all()

    def create(self, obj: ModelType) -> ModelType:
        """Persist a new entity into the database."""
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelType) -> ModelType:
        """Commit updates to an existing entity."""
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        """Delete an entity from the database."""
        self.db.delete(obj)
        self.db.commit()
