# backend/langchain_app/chains/ticket_escalation.py

from typing import Dict

# Simple trigger keywords for escalation
ESCALATION_KEYWORDS = [
    "not helpful", "need help", "speak to agent",
    "raise a ticket", "doesn't work", "contact support",
    "still broken", "frustrated", "not working", "complaint"
]

def should_escalate(user_input: str, bot_response: str, confidence_score: float = None) -> bool:
    """
    Determines whether the conversation should be escalated.
    
    Triggers:
    - Low confidence score (if available)
    - User says escalation-related phrases
    - Bot admits uncertainty
    """
    user_input = user_input.lower()
    bot_response = bot_response.lower()

    # Rule 1: Trigger keywords in user input
    for keyword in ESCALATION_KEYWORDS:
        if keyword in user_input:
            return True

    # Rule 2: LLM unsure (soft fallback phrase detection)
    if any(phrase in bot_response for phrase in ["i'm not sure", "i don't know", "can't help", "unable to answer"]):
        return True

    # Rule 3: Confidence (optional, if you calculate it later)
    if confidence_score is not None and confidence_score < 0.4:
        return True

    return False


def build_ticket_payload(
    user_input: str,
    customer_email: str,
    product: str,
    issue_summary: str
) -> Dict:
    """
    Creates a dictionary payload to raise a ticket (mock or real).
    """
    return {
        "email": customer_email,
        "product": product,
        "issue": issue_summary,
        "user_message": user_input,
        "status": "pending",
        "priority": "normal"
    }
