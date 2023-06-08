import uuid
from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, UUID_ID, GUID
from sqlalchemy import MetaData, Integer, String, TIMESTAMP, Boolean, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_file.storage import StorageManager
from src.database import Base
from sqlalchemy_file import FileField
from libcloud.storage.drivers.local import LocalStorageDriver
import os


class User(SQLAlchemyBaseUserTableUUID, Base):
    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, nullable=False)
    registered_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    file = relationship("Mp3FIle")



class Mp3FIle(Base):
    __tablename__ = "mp3file"
    id: Mapped[UUID_ID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    content = mapped_column(FileField())
    user_id  = mapped_column(GUID, ForeignKey("user.id", ondelete='CASCADE'), nullable=True)


os.makedirs("/tmp/storage/attachment", 0o777, exist_ok=True)
container = LocalStorageDriver("/tmp/storage").get_container("attachment")
StorageManager.add_storage("default", container)