import datetime
from typing import List, Dict, Any, Optional

# Simulated / Authorized Inbox
MOCK_INBOX = [
    {
        "id": "msg_001",
        "sender": "hiring@innovateai.tech",
        "subject": "Interview Invitation: Senior AI/ML Engineer Role",
        "date": "2026-11-16 14:30",
        "snippet": "We were impressed with your profile and projects on autonomous agents. We'd love to schedule a 45-minute technical discussion this Wednesday.",
        "is_important": True,
        "category": "Career"
    },
    {
        "id": "msg_002",
        "sender": "github-notifications@github.com",
        "subject": "Pull Request #42 merged in nikitha-ai",
        "date": "2026-11-16 11:15",
        "snippet": "nikitha14-dotcom merged 3 commits into main from feature/browser-agent.",
        "is_important": False,
        "category": "Development"
    },
    {
        "id": "msg_003",
        "sender": "newsletter@deeplearning.weekly",
        "subject": "State of Multimodal Reasoning & vLLM Optimizations",
        "date": "2026-11-15 09:00",
        "snippet": "This edition covers architectural breakthroughs in attention mechanisms and speculative decoding for low-latency inference.",
        "is_important": False,
        "category": "Newsletter"
    }
]

class EmailAssistantTool:
    @staticmethod
    def get_inbox_summary() -> List[Dict[str, Any]]:
        return MOCK_INBOX

    @staticmethod
    def draft_reply(email_id: str, tone: str = "professional") -> Dict[str, Any]:
        target = next((m for m in MOCK_INBOX if m["id"] == email_id), None)
        if not target:
            return {"error": "Email not found"}

        subject = f"Re: {target['subject']}"
        body = (
            f"Dear {target['sender'].split('@')[0].title()},\n\n"
            f"Thank you very much for reaching out regarding '{target['subject']}'.\n\n"
            "I would be delighted to connect. Wednesday afternoon works well for me between 2:00 PM and 5:00 PM IST. "
            "Please send along a calendar invitation at your convenience.\n\n"
            "Best regards,\n"
            "Nikitha"
        )
        return {
            "to": target["sender"],
            "subject": subject,
            "draft_body": body,
            "status": "draft_created",
            "safety_note": "Draft created. This email WILL NOT be sent without your explicit approval."
        }
