from enum import Enum


class SystemCapability(str, Enum):
    TICKETING = "ticketing"
    WEBHOOK_UPDATES = "webhook_updates"
    POLLING_UPDATES = "polling_updates"
    CHANNEL_NOTIFICATION_UPDATES = "channel_notification_updates"
    CREATE_CASE = "create_case"
    UPDATE_CASE = "update_case"
    ASSIGN_CASE = "assign_case"
    CLOSE_CASE = "close_case"
    REOPEN_CASE = "reopen_case"
