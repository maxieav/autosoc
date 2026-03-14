"""Threat detection: rule-based detection engine."""

import re


class Rule:
    """A detection rule with a name, pattern (regex), severity, and description."""

    def __init__(self, name: str, pattern: str, severity: str, description: str = ""):
        self.name = name
        self.pattern = pattern
        self.severity = severity
        self.description = description
        self._regex = re.compile(pattern, re.IGNORECASE)

    def matches(self, text: str) -> bool:
        """Return True if the rule pattern matches the given text."""
        return bool(self._regex.search(text))


class ThreatDetector:
    """Rule-based threat detector."""

    DEFAULT_RULES = [
        Rule(
            "brute_force",
            r"failed login|authentication failure|invalid password",
            "HIGH",
            "Brute force login attempt",
        ),
        Rule(
            "sql_injection",
            r"(?i)(select|union|insert|drop|delete)\s+.*from|'--|\bor\b\s+1=1",
            "CRITICAL",
            "SQL injection attempt",
        ),
        Rule(
            "port_scan",
            r"port scan|nmap|scanning ports",
            "MEDIUM",
            "Port scanning detected",
        ),
        Rule(
            "malware",
            r"malware|ransomware|trojan|virus detected",
            "CRITICAL",
            "Malware detected",
        ),
        Rule(
            "privilege_escalation",
            r"privilege escalation|sudo.*failed|su.*failed",
            "HIGH",
            "Privilege escalation attempt",
        ),
    ]

    def __init__(self, rules: list[Rule] | None = None):
        """Initialize with custom rules, or use DEFAULT_RULES if none provided."""
        self.rules: list[Rule] = list(rules) if rules is not None else list(self.DEFAULT_RULES)

    def add_rule(self, rule: Rule) -> None:
        """Add a detection rule."""
        self.rules.append(rule)

    def detect(self, entry: dict) -> list[dict]:
        """Check a parsed log entry against all rules.

        Returns a list of matches:
        [{"rule": rule.name, "severity": rule.severity, "description": rule.description}]
        """
        text = entry.get("message", "") + " " + entry.get("raw", "")
        matches = []
        for rule in self.rules:
            if rule.matches(text):
                matches.append(
                    {
                        "rule": rule.name,
                        "severity": rule.severity,
                        "description": rule.description,
                    }
                )
        return matches

    def scan(self, entries: list[dict]) -> list[dict]:
        """Scan multiple log entries.

        Returns list of dicts: {"entry": entry, "matches": [match, ...]}
        Only returns entries that had at least one match.
        """
        results = []
        for entry in entries:
            matches = self.detect(entry)
            if matches:
                results.append({"entry": entry, "matches": matches})
        return results
