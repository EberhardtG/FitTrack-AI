from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, func 
from app.db import Base
from datetime import datetime


class Weight(Base):
    """
    SQLAlchemy model for the weights table.
    """
    __tablename__ = "weights"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)
    # Assuming weight is in kilograms and has a reasonable maximum

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship("User", back_populates="weights")

    def __repr__(self):
        return f"<Weight id={self.id} value={self.value}>"
