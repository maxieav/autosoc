from enum import Enum


class ChannelCapability(str, Enum):
    SAME_THREAD = "same_thread"
    HTML = "html"
    MARKDOWN = "markdown"
    PLAIN = "plain"
    GROUPING = "grouping"


class NotificationType(str, Enum):
    CASE_CREATED = "case_created"
    CASE_UPDATED = "case_updated"
    CASE_CLOSED = "case_closed"
