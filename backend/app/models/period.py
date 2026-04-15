"""Registration period model."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Date, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class RegistrationPeriod(Base):
    __tablename__ = "registration_periods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="DRAFT")  # DRAFT, OPEN, CLOSED
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    proposals = relationship("Proposal", back_populates="registration_period")

    def __repr__(self):
        return f"<RegistrationPeriod {self.title} ({self.status})>"
