from typing import Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.security import ActionApproval

# Sensitive action types that strictly mandate human approval
SENSITIVE_ACTIONS = {
    "send_email": "Send Outbound Email",
    "apply_job": "Submit Job Application",
    "submit_form": "Submit Web Form with Personal Data",
    "delete_file": "Delete File or Project Resource",
    "financial_action": "Execute Financial or Payment Operation",
    "change_settings": "Modify System Security Credentials",
}

async def check_or_request_approval(
    db: AsyncSession,
    action_type: str,
    title: str,
    description: str,
    payload: Dict[str, Any],
    agent_name: str = "orchestrator",
    explicit_approval_id: int = None
) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Checks if an action requires human approval.
    If it requires approval and no valid approved ID is provided, creates a pending ActionApproval
    and returns (False, message, approval_record).
    """
    if action_type not in SENSITIVE_ACTIONS:
        return True, "Safe action approved for automatic execution", {}

    if explicit_approval_id:
        approval = await db.get(ActionApproval, explicit_approval_id)
        if approval and approval.status == "approved":
            approval.status = "executed"
            await db.commit()
            return True, f"Action '{title}' was explicitly approved by user.", {"approval_id": approval.id}
        else:
            return False, "Action requires user approval but approval status is invalid.", {}

    # Create a pending approval request
    pending = ActionApproval(
        action_type=action_type,
        title=title,
        description=description,
        agent_name=agent_name,
        payload=payload,
        status="pending"
    )
    db.add(pending)
    await db.commit()
    await db.refresh(pending)

    return False, (
        f"SAFETY GUARD ACTIVATED: This action requires your explicit confirmation before execution.\n"
        f"Action: {title}\n"
        f"Details: {description}\n"
        f"Please approve or reject this request in the Approvals panel."
    ), {
        "approval_id": pending.id,
        "action_type": action_type,
        "title": title,
        "status": "pending"
    }
