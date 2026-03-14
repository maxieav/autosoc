"""Log analysis: parse log lines, extract fields."""

import re

# Matches: "2024-01-15 10:30:00 ERROR message" or "2024-01-15T10:30:00 ERROR message"
_TIMESTAMP_LEVEL_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)\s+"
    r"(DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+(.*)",
    re.IGNORECASE,
)

# Matches: "[ERROR] message" or "[ERROR]: message"
_BRACKET_LEVEL_RE = re.compile(
    r"^\[(DEBUG|INFO|WARNING|ERROR|CRITICAL)\]\s*:?\s*(.*)",
    re.IGNORECASE,
)

# Matches: "ERROR: message" or "INFO: message"
_PREFIX_LEVEL_RE = re.compile(
    r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)\s*:\s*(.*)",
    re.IGNORECASE,
)

_VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


class LogAnalyzer:
    """Parses and analyzes log entries."""

    def parse_line(self, line: str) -> dict:
        """Parse a log line into a structured dict.

        Supports formats:
        - "2024-01-15 10:30:00 ERROR Failed login attempt"
        - "[ERROR] Failed login attempt"
        - "INFO: Service started"
        """
        raw = line.rstrip("\n")

        m = _TIMESTAMP_LEVEL_RE.match(raw)
        if m:
            return {
                "timestamp": m.group(1),
                "level": m.group(2).upper(),
                "message": m.group(3),
                "raw": raw,
            }

        m = _BRACKET_LEVEL_RE.match(raw)
        if m:
            return {
                "timestamp": "",
                "level": m.group(1).upper(),
                "message": m.group(2),
                "raw": raw,
            }

        m = _PREFIX_LEVEL_RE.match(raw)
        if m:
            return {
                "timestamp": "",
                "level": m.group(1).upper(),
                "message": m.group(2),
                "raw": raw,
            }

        return {
            "timestamp": "",
            "level": "INFO",
            "message": raw,
            "raw": raw,
        }

    def analyze(self, lines: list[str]) -> list[dict]:
        """Parse multiple log lines and return list of parsed entries."""
        return [self.parse_line(line) for line in lines]

    def filter_by_level(self, entries: list[dict], level: str) -> list[dict]:
        """Filter entries by log level (case-insensitive)."""
        target = level.upper()
        return [e for e in entries if e.get("level", "").upper() == target]

    def count_by_level(self, entries: list[dict]) -> dict:
        """Return a dict of {level: count} for all entries."""
        counts: dict[str, int] = {}
        for entry in entries:
            lvl = entry.get("level", "INFO").upper()
            counts[lvl] = counts.get(lvl, 0) + 1
        return counts
