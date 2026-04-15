"""Acceptance dossier and acceptance review models."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class AcceptanceDossier(Base):
    __tablename__ = "acceptance_dossiers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id = Column(UUID(as_uuid=True), ForeignKey("proposals.id"), nullable=False)
    final_report = Column(Text, nullable=False)
    achievements = Column(Text, nullable=False)
    publications = Column(Text, nullable=True)  # Simple text field for MVP
    status = Column(String(30), nullable=False, default="SUBMITTED")  # SUBMITTED, REVISION_REQUESTED, UNDER_REVIEW, PASSED, FAILED
    revision_reason = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    proposal = relationship("Proposal", back_populates="acceptance_dossiers")
    acceptance_reviews = relationship("AcceptanceReview", back_populates="dossier")

    def __repr__(self):
        return f"<AcceptanceDossier ({self.status})>"


class AcceptanceReview(Base):
    __tablename__ = "acceptance_reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dossier_id = Column(UUID(as_uuid=True), ForeignKey("acceptance_dossiers.id"), nullable=False)
    council_id = Column(UUID(as_uuid=True), ForeignKey("councils.id"), nullable=False)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    score = Column(Float, nullable=True)  # 0-100
    comments = Column(Text, nullable=True)
    verdict = Column(String(20), nullable=True)  # PASS, FAIL
    status = Column(String(20), nullable=False, default="PENDING")  # PENDING, SUBMITTED
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    dossier = relationship("AcceptanceDossier", back_populates="acceptance_reviews")
    council = relationship("Council", back_populates="acceptance_reviews")
    reviewer = relationship("User", back_populates="acceptance_reviews")

    def __repr__(self):
        return f"<AcceptanceReview by {self.reviewer_id} ({self.status})>"
