"""Incident management: create, track, and update security incidents."""

import uuid
from datetime import datetime, timezone
from enum import Enum


class Severity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Status(Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class Incident:
    """Represents a security incident."""

    def __init__(self, title: str, severity: Severity, description: str = ""):
        self.id = str(uuid.uuid4())
        self.title = title
        self.severity = severity
        self.description = description
        self.status = Status.OPEN
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = self.created_at
        self.notes: list[str] = []

    def update_status(self, status: Status) -> None:
        """Update status and updated_at."""
        self.status = status
        self.updated_at = datetime.now(timezone.utc)

    def add_note(self, note: str) -> None:
        """Append a note and update updated_at."""
        self.notes.append(note)
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """Serialize to dict with all fields (datetimes as ISO strings)."""
        return {
            "id": self.id,
            "title": self.title,
            "severity": self.severity.value,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "notes": list(self.notes),
        }


class IncidentManager:
    """Manages a collection of incidents."""

    def __init__(self):
        self._incidents: dict[str, Incident] = {}

    def create(self, title: str, severity: Severity | str, description: str = "") -> Incident:
        """Create and store a new incident. severity can be a Severity enum or string."""
        if isinstance(severity, str):
            severity = Severity(severity.upper())
        incident = Incident(title=title, severity=severity, description=description)
        self._incidents[incident.id] = incident
        return incident

    def get(self, incident_id: str) -> Incident | None:
        """Get an incident by ID."""
        return self._incidents.get(incident_id)

    def list_all(self) -> list[Incident]:
        """Return all incidents sorted by created_at descending."""
        return sorted(self._incidents.values(), key=lambda i: i.created_at, reverse=True)

    def list_by_status(self, status: Status | str) -> list[Incident]:
        """Filter incidents by status."""
        if isinstance(status, str):
            status = Status(status.upper())
        return [i for i in self.list_all() if i.status == status]

    def list_by_severity(self, severity: Severity | str) -> list[Incident]:
        """Filter incidents by severity."""
        if isinstance(severity, str):
            severity = Severity(severity.upper())
        return [i for i in self.list_all() if i.severity == severity]

    def resolve(self, incident_id: str) -> bool:
        """Mark incident as RESOLVED. Returns True if found, False otherwise."""
        incident = self._incidents.get(incident_id)
        if incident is None:
            return False
        incident.update_status(Status.RESOLVED)
        return True

    def close(self, incident_id: str) -> bool:
        """Mark incident as CLOSED. Returns True if found, False otherwise."""
        incident = self._incidents.get(incident_id)
        if incident is None:
            return False
        incident.update_status(Status.CLOSED)
        return True

    def from_detections(self, detections: list[dict]) -> list[Incident]:
        """Create incidents from ThreatDetector.scan() output.

        For each detection with matches, creates one incident per match.
        Title format: f"[{match['severity']}] {match['description']}"
        Description: the log entry's raw field.
        Returns list of created incidents.
        """
        created: list[Incident] = []
        for detection in detections:
            entry = detection.get("entry", {})
            raw = entry.get("raw", "")
            for match in detection.get("matches", []):
                title = f"[{match['severity']}] {match['description']}"
                incident = self.create(
                    title=title,
                    severity=match["severity"],
                    description=raw,
                )
                created.append(incident)
        return created
