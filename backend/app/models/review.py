"""Review model for proposal reviews."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    council_id = Column(UUID(as_uuid=True), ForeignKey("councils.id"), nullable=False)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    proposal_id = Column(UUID(as_uuid=True), ForeignKey("proposals.id"), nullable=False)
    score = Column(Float, nullable=True)  # 0-100
    comments = Column(Text, nullable=True)
    verdict = Column(String(20), nullable=True)  # PASS, FAIL, NEEDS_REVISION
    status = Column(String(20), nullable=False, default="PENDING")  # PENDING, SUBMITTED
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    council = relationship("Council", back_populates="reviews")
    reviewer = relationship("User", back_populates="reviews")
    proposal = relationship("Proposal", back_populates="reviews")

    def __repr__(self):
        return f"<Review by {self.reviewer_id} - {self.status}>"
