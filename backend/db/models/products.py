from uuid import uuid4

from db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Product(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nom = Column(String, nullable=False)
    cathegorie = Column(String, nullable=True)
    description = Column(String, nullable=True)
    url_image = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    owner = relationship("User", back_populates="products")
