# Author: Sanidayal Gupta
import uuid
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.config import settings
from app.database import engine, Base, get_db
from app.models import TransactionLedger
from app.schemas import TransactionAuthRequest, TransactionAuthResponse
from app.agent import run_aml_fraud_investigation

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description=f"Authored by {settings.AUTHOR}. Real-Time BFSI Fraud Shield with Google GenAI & MCP."
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "lead_architect": settings.AUTHOR,
        "environment": settings.ENVIRONMENT
    }

@app.post("/api/v1/transactions/authorize", response_model=TransactionAuthResponse, status_code=status.HTTP_200_OK)
async def authorize_transaction(
    payload: TransactionAuthRequest,
    db: AsyncSession = Depends(get_db)
):
    # 1. Run agentic AML & Fraud triage
    raw_data = payload.model_dump()
    raw_data["amount"] = float(payload.amount)
    investigation = await run_aml_fraud_investigation(raw_data)

    txn_id = str(uuid.uuid4())

    # 2. Record decision in ACID Transaction Ledger
    ledger_entry = TransactionLedger(
        txn_uuid=txn_id,
        account_number=payload.account_id,
        amount=payload.amount,
        currency=payload.currency,
        merchant_name=payload.merchant_name,
        merchant_mcc=payload.merchant_category_code,
        decision=investigation.get("decision", "APPROVED"),
        risk_score=investigation.get("risk_score", 10),
        audit_notes=investigation.get("reasoning")
    )
    db.add(ledger_entry)
    await db.commit()

    return TransactionAuthResponse(
        transaction_id=txn_id,
        decision=ledger_entry.decision,
        risk_score=ledger_entry.risk_score,
        forensic_reasoning=ledger_entry.audit_notes,
        mcp_actions_triggered=investigation.get("executed_tools", []),
        authorized_at=datetime.utcnow()
    )
