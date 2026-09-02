# Author: Sanidayal Gupta
# Module: Autonomous AML Investigator Agent (Powered by Google GenAI SDK & MCP)
import json
import logging
from app.config import settings
from app.mcp_tools import BFSIMCPRegistry

logger = logging.getLogger("uvicorn.error")

try:
    from google import genai
    genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    logger.warning(f"Google GenAI SDK awaiting API key credentials: {e}")
    genai_client = None

async def run_aml_fraud_investigation(txn_data: dict) -> dict:
    tools_spec = BFSIMCPRegistry.get_tool_definitions()

    system_instruction = (
        "You are an autonomous Principal Banking Fraud & AML Compliance Investigator. "
        "Evaluate incoming financial transactions for smurfing, account takeover, carding, or regulatory sanctions violations. "
        "Determine the final decision (APPROVED, REJECT_AND_FREEZE, STEP_UP_REQUIRED), calculate a risk score (0-100), "
        "and select which standardized MCP banking tools to invoke.\n\n"
        f"Available MCP Tools:\n{json.dumps(tools_spec)}\n\n"
        "Return ONLY a valid JSON object matching this schema:\n"
        "{\n"
        "  \"decision\": \"APPROVED\" | \"REJECT_AND_FREEZE\" | \"STEP_UP_REQUIRED\",\n"
        "  \"risk_score\": int,\n"
        "  \"reasoning\": \"Forensic justification for compliance audit\",\n"
        "  \"tools_to_run\": [\n"
        "    {\"tool_name\": \"tool_name_from_registry\", \"arguments\": {\"arg_key\": \"arg_val\"}}\n"
        "  ]\n"
        "}"
    )

    user_prompt = f"TRANSACTION PAYLOAD UNDER REVIEW:\n{json.dumps(txn_data)}"

    parsed_plan = None
    if genai_client and settings.GEMINI_API_KEY != "mock-key-for-local-dev":
        try:
            res = genai_client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=f"{system_instruction}\n\n{user_prompt}",
                config={"response_mime_type": "application/json"}
            )
            parsed_plan = json.loads(res.text)
        except Exception as err:
            logger.error(f"Google GenAI SDK AML investigation error: {err}")

    # Deterministic fallback for immediate local testing
    if not parsed_plan:
        mcc = str(txn_data.get("merchant_category_code", ""))
        amt = float(txn_data.get("amount", 0.0))
        is_crypto_or_wire = mcc in ["6051", "4829"] or "crypto" in str(txn_data.get("merchant_name", "")).lower()
        is_high = amt >= 50000.0 or txn_data.get("is_new_device", False)

        if is_crypto_or_wire and is_high:
            parsed_plan = {
                "decision": "REJECT_AND_FREEZE",
                "risk_score": 92,
                "reasoning": "High-risk MCC coupled with newly paired device and large transaction value exceeding velocity limits.",
                "tools_to_run": [
                    {
                        "tool_name": "freeze_payment_instrument",
                        "arguments": {
                            "account_number": txn_data.get("account_id"),
                            "reason": "Anomalous high-value payment to crypto gateway from unrecognized endpoint."
                        }
                    },
                    {
                        "tool_name": "file_regulatory_sar",
                        "arguments": {
                            "account_number": txn_data.get("account_id"),
                            "red_flag_category": "STRUCTURING",
                            "narrative": "Suspicious rapid fund diversion flag raised."
                        }
                    }
                ]
            }
        else:
            parsed_plan = {
                "decision": "APPROVED",
                "risk_score": 12,
                "reasoning": "Transaction aligns with baseline behavioral parameters and low-risk merchant profile.",
                "tools_to_run": []
            }

    # Execute tools via MCP Registry
    executed_tools = []
    for action in parsed_plan.get("tools_to_run", []):
        t_name = action.get("tool_name")
        t_args = action.get("arguments", {})
        exec_res = await BFSIMCPRegistry.execute_tool(t_name, t_args)
        executed_tools.append(exec_res)

    return {
        "decision": parsed_plan.get("decision", "APPROVED"),
        "risk_score": parsed_plan.get("risk_score", 10),
        "reasoning": parsed_plan.get("reasoning", "Standard authorization."),
        "executed_tools": executed_tools
    }
