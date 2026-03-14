from enum import Enum


class ConnectorType(str, Enum):
    SERVICENOW = "servicenow"
    JIRA = "jira"
    PAGERDUTY = "pagerduty"
    GENERIC = "generic"
