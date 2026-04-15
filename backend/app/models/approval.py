"""Approval decision model."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class ApprovalDecision(Base):
    __tablename__ = "approval_decisions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id = Column(UUID(as_uuid=True), ForeignKey("proposals.id"), nullable=False)
    decided_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    decision = Column(String(20), nullable=False)  # APPROVED, REJECTED
    reason = Column(Text, nullable=True)
    decided_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    proposal = relationship("Proposal", back_populates="approval_decisions")
    decided_by_user = relationship("User", back_populates="approval_decisions")

    def __repr__(self):
        return f"<ApprovalDecision {self.decision}>"
