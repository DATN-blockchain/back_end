from typing import Any

from app.constant.template import NotificationTemplate
from app.model.base import NotificationType
from app.services import NotificationService


async def send_notification(
        notification_service: NotificationService,
        entity: Any,
        notification_type: NotificationType,
        message_template: NotificationTemplate,
        action: str,
        current_user: Any = None,
        owner: Any = None
):
    await notification_service.notify_entity_status(
        entity=entity,
        notification_type=notification_type,
        message_template=message_template,
        action=action,
        current_user=current_user,
        owner=owner,
    )
