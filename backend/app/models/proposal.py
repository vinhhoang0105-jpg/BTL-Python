"""Proposal model with status history tracking."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    objectives = Column(Text, nullable=True)
    methodology = Column(Text, nullable=True)
    expected_outcomes = Column(Text, nullable=True)
    duration_months = Column(Integer, nullable=True)

    pi_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    field_id = Column(UUID(as_uuid=True), ForeignKey("research_fields.id"), nullable=True)
    period_id = Column(UUID(as_uuid=True), ForeignKey("registration_periods.id"), nullable=True)

    status = Column(String(40), nullable=False, default="DRAFT")
    revision_reason = Column(Text, nullable=True)  # Reason when returned for revision
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    principal_investigator = relationship("User", back_populates="proposals_as_pi", foreign_keys=[pi_id])
    research_field = relationship("ResearchField", back_populates="proposals")
    registration_period = relationship("RegistrationPeriod", back_populates="proposals")
    members = relationship("ProposalMember", back_populates="proposal", cascade="all, delete-orphan")
    councils = relationship("Council", back_populates="proposal")
    reviews = relationship("Review", back_populates="proposal")
    approval_decisions = relationship("ApprovalDecision", back_populates="proposal")
    progress_reports = relationship("ProgressReport", back_populates="proposal", order_by="ProgressReport.report_order")
    acceptance_dossiers = relationship("AcceptanceDossier", back_populates="proposal")
    status_history = relationship("ProposalStatusHistory", back_populates="proposal", order_by="ProposalStatusHistory.changed_at")

    def __repr__(self):
        return f"<Proposal {self.title[:50]} ({self.status})>"


class ProposalMember(Base):
    """Co-investigators on a proposal."""
    __tablename__ = "proposal_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id = Column(UUID(as_uuid=True), ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role_in_proposal = Column(String(50), default="CO_INVESTIGATOR")  # CO_INVESTIGATOR, CONSULTANT

    # Relationships
    proposal = relationship("Proposal", back_populates="members")
    user = relationship("User", back_populates="proposal_memberships")


class ProposalStatusHistory(Base):
    """Audit log for proposal status changes."""
    __tablename__ = "proposal_status_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id = Column(UUID(as_uuid=True), ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False)
    from_status = Column(String(40), nullable=True)  # null for initial creation
    to_status = Column(String(40), nullable=False)
    action = Column(String(50), nullable=False)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # null for SYSTEM
    note = Column(Text, nullable=True)
    changed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    proposal = relationship("Proposal", back_populates="status_history")
