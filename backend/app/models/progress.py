"""Progress report model."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class ProgressReport(Base):
    __tablename__ = "progress_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id = Column(UUID(as_uuid=True), ForeignKey("proposals.id"), nullable=False)
    submitted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    report_order = Column(Integer, nullable=False)  # auto-incremented per proposal
    content = Column(Text, nullable=False)
    completion_percentage = Column(Float, nullable=False)  # 0-100
    issues = Column(Text, nullable=True)
    next_steps = Column(Text, nullable=False)
    submitted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    proposal = relationship("Proposal", back_populates="progress_reports")
    submitted_by_user = relationship("User", back_populates="progress_reports")

    def __repr__(self):
        return f"<ProgressReport #{self.report_order} - {self.completion_percentage}%>"
