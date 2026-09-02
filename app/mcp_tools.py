# Author: Sanidayal Gupta
# Module: MCP (Model Context Protocol) Standardized Tool Contracts for Core Banking
from typing import Dict, Any, List

class BFSIMCPRegistry:
    @staticmethod
    def get_tool_definitions() -> List[Dict[str, Any]]:
        return [
            {
                "name": "freeze_payment_instrument",
                "description": "Places an immediate security lock on an account or payment card.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_number": {"type": "string", "description": "Target bank account number"},
                        "reason": {"type": "string", "description": "AML/Fraud detection justification"}
                    },
                    "required": ["account_number", "reason"]
                }
            },
            {
                "name": "trigger_step_up_biometric_auth",
                "description": "Pushes an out-of-band mobile biometric verification prompt to the cardholder.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_number": {"type": "string", "description": "Target account number"},
                        "txn_id": {"type": "string", "description": "Inflight transaction UUID"}
                    },
                    "required": ["account_number", "txn_id"]
                }
            },
            {
                "name": "file_regulatory_sar",
                "description": "Pre-files an electronic Suspicious Activity Report (SAR) for compliance review.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_number": {"type": "string", "description": "Account number"},
                        "red_flag_category": {"type": "string", "description": "STRUCTURING, UNKNOWN_BENEFICIARY, SANCTION_BREACH"},
                        "narrative": {"type": "string", "description": "Detailed explanation"}
                    },
                    "required": ["account_number", "red_flag_category", "narrative"]
                }
            }
        ]

    @staticmethod
    async def execute_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if name == "freeze_payment_instrument":
            acc = arguments.get("account_number")
            return {
                "account_number": acc,
                "freeze_status": "LOCKED",
                "hold_reference": "SEC-HOLD-89123",
                "message": f"Instrument for account {acc} temporarily suspended."
            }
        elif name == "trigger_step_up_biometric_auth":
            acc = arguments.get("account_number")
            return {
                "account_number": acc,
                "auth_challenge": "BIOMETRIC_PUSH_SENT",
                "ttl_seconds": 90,
                "status": "CHALLENGE_ISSUED"
            }
        elif name == "file_regulatory_sar":
            acc = arguments.get("account_number")
            cat = arguments.get("red_flag_category", "AML_SUSPICION")
            return {
                "sar_case_id": f"SAR-FIN-{acc[-5:]}-AUTO",
                "filing_status": "QUEUED_FOR_OFFICER_SIGN",
                "category": cat
            }
        return {"error": f"Unknown MCP tool contract: {name}"}
