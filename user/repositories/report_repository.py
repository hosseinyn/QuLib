from ..models import DeleteAccount
from typing import Optional

def create_delete_account_report(reason: Optional[str]) -> None:
    """
    Create a delete account report with the reason provided.

    Args:
        reason (Optional[str]): The reason given for account deletion.

    document by AI
    """
    DeleteAccount.objects.create(reason=reason)