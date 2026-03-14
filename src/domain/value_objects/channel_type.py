from enum import Enum


class ChannelType(str, Enum):
    EMAIL = "email"
    SLACK = "slack"
    WHATSAPP = "whatsapp"
    TEAMS = "teams"
    GENERIC = "generic"
