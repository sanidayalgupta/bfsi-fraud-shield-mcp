# Author: Sanidayal Gupta
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

class TransactionAuthRequest(BaseModel):
    account_id: str = Field(..., example="ACC-IND-99120")
    card_last_four: str = Field(..., example="4819")
    amount: Decimal = Field(..., example=85000.00)
    currency: str = Field("INR", example="INR")
    merchant_name: str = Field(..., example="CryptoExchange Global Intl")
    merchant_category_code: str = Field(..., example="6051")
    device_ip: str = Field("185.220.101.5", example="185.220.101.5")
    is_new_device: bool = Field(True, example=True)

class TransactionAuthResponse(BaseModel):
    transaction_id: str
    decision: str
    risk_score: int
    forensic_reasoning: str
    mcp_actions_triggered: List[Dict[str, Any]]
    authorized_at: datetime
