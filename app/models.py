# Author: Sanidayal Gupta
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, Boolean, JSON, func
from app.database import Base

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(50), unique=True, index=True, nullable=False)
    account_holder_name = Column(String(100), nullable=False)
    risk_tier = Column(String(20), default="STANDARD")  # STANDARD, WATCHLIST, PEP, HIGH_RISK
    is_frozen = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TransactionLedger(Base):
    __tablename__ = "transaction_ledger"

    id = Column(Integer, primary_key=True, index=True)
    txn_uuid = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, index=True)
    account_number = Column(String(50), index=True, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default="INR")
    merchant_name = Column(String(100), nullable=False)
    merchant_mcc = Column(String(10), nullable=False)
    decision = Column(String(30), default="APPROVED")  # APPROVED, REJECTED, STEP_UP_REQUIRED
    risk_score = Column(Integer, default=10)
    audit_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SuspiciousActivityReport(Base):
    __tablename__ = "suspicious_activity_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_code = Column(String(50), unique=True, index=True, nullable=False)
    account_number = Column(String(50), index=True, nullable=False)
    transaction_id = Column(String(36), nullable=False)
    narrative = Column(Text, nullable=False)
    severity = Column(String(20), default="HIGH")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
