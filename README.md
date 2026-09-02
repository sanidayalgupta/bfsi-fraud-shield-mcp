# Autonomous BFSI Real-Time Fraud & AML Transaction Shield 🏦💳⚡

**Author:** Sanidayal Gupta  
**Contact:** sanidayalgupta10799@gmail.com | [LinkedIn](https://linkedin.com/in/sanidayalgupta)

---

An asynchronous, production-grade financial fraud detection, anti-money laundering (AML), and transaction sanction screener built for the **Banking, Financial Services, and Insurance (BFSI)** industry.

Engineered with **FastAPI**, **PostgreSQL (Asyncpg + SQLAlchemy 2.0)**, **Redis (Atomic Sliding Window Token/Velocity Checks)**, the **Google GenAI SDK (`google-genai`)**, and standardized **Model Context Protocol (MCP)** tool contracts.

---

## 🛑 The Real-World BFSI Problem

In modern retail banking and digital payments (UPI, Card Rails, SWIFT/FedNow):
1. **Smurfing & Structuring Velocity:** Fraud syndicates split large illicit funds into multiple micro-transactions under ₹50,000 ($600) across short intervals to evade standard threshold audits.
2. **Account Takeover & Device Drift:** Transactions initiate from uncharacteristic IP geolocations or new device fingerprints shortly after credential resets.
3. **High False-Positive Latency:** Legacy rule engines block genuine customer payments or take hours to manually review suspicious activity, hurting customer retention.
4. **Audit Immutability & Compliance:** Regulatory frameworks (RBI, FinCEN, FATF) require explainable, tamper-proof audit trails for every flagged or blocked transaction.

---

## 💡 The Solution: Autonomous Banking Fraud Shield

* **Sub-50ms Velocity & Behavioral Screening:** Redis-backed sliding-window meters track volume and velocity per cardholder before committing funds.
* **Autonomous GenAI AML Agent:** Transactions triggering multi-factor risk flags are routed to an agentic reasoning loop using the **Google GenAI SDK (Gemini)**. The model evaluates behavioral context, risk factors, and sanctions profiles.
* **Standardized MCP Tool Orchestration:** The agent verifies customer credit standings, places instant temporary card freezes, or dispatches suspicious activity reports (SARs) via standardized **Model Context Protocol (MCP)** adapters.
* **ACID Immutable Ledger:** Every authorization decision, velocity metric, and agent reasoning step is written to a PostgreSQL database using asynchronous connection pooling.

---

## 🏗️ System Architecture Flow

```
   [ Payment Gateway / Core Banking Switch Webhook ]
                          │
                          ▼
               [ FastAPI Ingestion API ]
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
[ Redis Velocity Cache ]         [ PostgreSQL Ledger ]
(Sliding Window Check)           (ACID Balance & Txns)
         │                                 │
         └────────────────┬────────────────┘
                          ▼
           [ Risk Flag Trigger Threshold? ]
                          │
                          ▼ (Yes: Route to Agent)
          [ Autonomous AML Investigator Agent ]
          (Google GenAI SDK — Gemini 2.5 Flash)
                          │
             [ MCP Standard Tool Router ]
                          │
       ┌──────────────────┼──────────────────┐
       ▼                  ▼                  ▼
[ Freeze Account ] [ Request Step-Up 2FA ] [ File SAR Report ]
       │                  │                  │
       └──────────────────┴──────────────────┘
                          │
                          ▼
         [ Immutable Compliance Audit Trail ]
```

---

## 🚀 Setup & Execution Guide

### 1. Environment & Dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Credentials
```bash
cp .env.example .env
```
Provide your `GEMINI_API_KEY` and update your PostgreSQL/Redis connection strings.

### 3. Run the Backend API
```bash
uvicorn app.main:app --reload --port 8000
```

Access the interactive OpenAPI Swagger documentation at: `http://127.0.0.1:8000/docs`

---

## 📋 End-to-End Practical Example

**Inspect an Inflight Payment:**
`POST /api/v1/transactions/authorize`

```json
{
  "account_id": "ACC-IND-99120",
  "card_last_four": "4819",
  "amount": 85000.00,
  "currency": "INR",
  "merchant_name": "CryptoExchange Global Intl",
  "merchant_category_code": "6051",
  "device_ip": "185.220.101.5",
  "is_new_device": true
}
```

**Agentic Output:**
* **Decision:** `REJECT_AND_FREEZE`
* **Risk Score:** `92 / 100 (CRITICAL)`
* **Reasoning:** High-risk MCC (Crypto), unusual IP range (known VPN/proxy exit node), newly paired device, and single-ticket amount exceeding historical 30-day baseline by 700%.
* **MCP Tools Invoked:** `freeze_payment_instrument`, `notify_account_holder_sms`.
