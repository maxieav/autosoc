"""Tests for autosoc.incident."""

import time
import pytest
from autosoc.incident import Incident, IncidentManager, Severity, Status


class TestSeverityEnum:
    def test_values(self):
        assert Severity.LOW.value == "LOW"
        assert Severity.MEDIUM.value == "MEDIUM"
        assert Severity.HIGH.value == "HIGH"
        assert Severity.CRITICAL.value == "CRITICAL"

    def test_from_string(self):
        assert Severity("HIGH") == Severity.HIGH


class TestStatusEnum:
    def test_values(self):
        assert Status.OPEN.value == "OPEN"
        assert Status.INVESTIGATING.value == "INVESTIGATING"
        assert Status.RESOLVED.value == "RESOLVED"
        assert Status.CLOSED.value == "CLOSED"


class TestIncident:
    def test_defaults(self):
        inc = Incident("Test incident", Severity.HIGH)
        assert inc.title == "Test incident"
        assert inc.severity == Severity.HIGH
        assert inc.status == Status.OPEN
        assert inc.description == ""
        assert inc.notes == []
        assert inc.id is not None
        assert inc.created_at == inc.updated_at

    def test_unique_ids(self):
        a = Incident("A", Severity.LOW)
        b = Incident("B", Severity.LOW)
        assert a.id != b.id

    def test_update_status(self):
        inc = Incident("T", Severity.MEDIUM)
        original_updated = inc.updated_at
        time.sleep(0.01)
        inc.update_status(Status.INVESTIGATING)
        assert inc.status == Status.INVESTIGATING
        assert inc.updated_at >= original_updated

    def test_add_note(self):
        inc = Incident("T", Severity.LOW)
        inc.add_note("First note")
        inc.add_note("Second note")
        assert inc.notes == ["First note", "Second note"]

    def test_add_note_updates_updated_at(self):
        inc = Incident("T", Severity.LOW)
        original = inc.updated_at
        time.sleep(0.01)
        inc.add_note("note")
        assert inc.updated_at >= original

    def test_to_dict(self):
        inc = Incident("Title", Severity.CRITICAL, "desc")
        d = inc.to_dict()
        assert d["title"] == "Title"
        assert d["severity"] == "CRITICAL"
        assert d["description"] == "desc"
        assert d["status"] == "OPEN"
        assert d["notes"] == []
        assert "id" in d
        assert "created_at" in d
        assert "updated_at" in d

    def test_to_dict_datetime_as_iso_string(self):
        inc = Incident("T", Severity.HIGH)
        d = inc.to_dict()
        # Should be parseable ISO strings
        from datetime import datetime
        datetime.fromisoformat(d["created_at"])
        datetime.fromisoformat(d["updated_at"])


class TestIncidentManager:
    @pytest.fixture
    def manager(self):
        return IncidentManager()

    def test_create_returns_incident(self, manager):
        inc = manager.create("Test", Severity.HIGH)
        assert isinstance(inc, Incident)
        assert inc.title == "Test"

    def test_create_with_string_severity(self, manager):
        inc = manager.create("T", "critical")
        assert inc.severity == Severity.CRITICAL

    def test_create_with_description(self, manager):
        inc = manager.create("T", Severity.LOW, description="details")
        assert inc.description == "details"

    def test_get_existing(self, manager):
        inc = manager.create("T", Severity.MEDIUM)
        retrieved = manager.get(inc.id)
        assert retrieved is inc

    def test_get_nonexistent(self, manager):
        assert manager.get("no-such-id") is None

    def test_list_all_sorted_desc(self, manager):
        a = manager.create("A", Severity.LOW)
        time.sleep(0.01)
        b = manager.create("B", Severity.MEDIUM)
        time.sleep(0.01)
        c = manager.create("C", Severity.HIGH)
        result = manager.list_all()
        assert result[0] is c
        assert result[1] is b
        assert result[2] is a

    def test_list_all_empty(self, manager):
        assert manager.list_all() == []

    def test_list_by_status(self, manager):
        open_inc = manager.create("Open", Severity.LOW)
        inv_inc = manager.create("Inv", Severity.MEDIUM)
        inv_inc.update_status(Status.INVESTIGATING)
        open_results = manager.list_by_status(Status.OPEN)
        assert open_inc in open_results
        assert inv_inc not in open_results

    def test_list_by_status_string(self, manager):
        inc = manager.create("T", Severity.LOW)
        result = manager.list_by_status("open")
        assert inc in result

    def test_list_by_severity(self, manager):
        high = manager.create("H", Severity.HIGH)
        low = manager.create("L", Severity.LOW)
        result = manager.list_by_severity(Severity.HIGH)
        assert high in result
        assert low not in result

    def test_list_by_severity_string(self, manager):
        inc = manager.create("T", Severity.CRITICAL)
        result = manager.list_by_severity("critical")
        assert inc in result

    def test_resolve_existing(self, manager):
        inc = manager.create("T", Severity.HIGH)
        assert manager.resolve(inc.id) is True
        assert inc.status == Status.RESOLVED

    def test_resolve_nonexistent(self, manager):
        assert manager.resolve("ghost-id") is False

    def test_close_existing(self, manager):
        inc = manager.create("T", Severity.MEDIUM)
        assert manager.close(inc.id) is True
        assert inc.status == Status.CLOSED

    def test_close_nonexistent(self, manager):
        assert manager.close("ghost-id") is False


class TestFromDetections:
    @pytest.fixture
    def manager(self):
        return IncidentManager()

    def _make_detection(self, raw: str, matches: list[dict]) -> dict:
        return {
            "entry": {"raw": raw, "message": raw, "level": "ERROR", "timestamp": ""},
            "matches": matches,
        }

    def test_creates_one_incident_per_match(self, manager):
        detections = [
            self._make_detection(
                "failed login attempt",
                [
                    {"rule": "brute_force", "severity": "HIGH", "description": "Brute force login attempt"},
                ],
            ),
            self._make_detection(
                "SELECT * FROM users",
                [
                    {"rule": "sql_injection", "severity": "CRITICAL", "description": "SQL injection attempt"},
                ],
            ),
        ]
        incidents = manager.from_detections(detections)
        assert len(incidents) == 2

    def test_multiple_matches_per_entry(self, manager):
        detections = [
            self._make_detection(
                "failed login privilege escalation",
                [
                    {"rule": "brute_force", "severity": "HIGH", "description": "Brute force login attempt"},
                    {"rule": "privilege_escalation", "severity": "HIGH", "description": "Privilege escalation attempt"},
                ],
            )
        ]
        incidents = manager.from_detections(detections)
        assert len(incidents) == 2

    def test_title_format(self, manager):
        detections = [
            self._make_detection(
                "ransomware detected",
                [{"rule": "malware", "severity": "CRITICAL", "description": "Malware detected"}],
            )
        ]
        incidents = manager.from_detections(detections)
        assert incidents[0].title == "[CRITICAL] Malware detected"

    def test_description_is_raw(self, manager):
        raw = "2024-01-01 00:00:00 ERROR ransomware detected in /tmp/payload"
        detections = [
            self._make_detection(
                raw,
                [{"rule": "malware", "severity": "CRITICAL", "description": "Malware detected"}],
            )
        ]
        incidents = manager.from_detections(detections)
        assert incidents[0].description == raw

    def test_incidents_stored_in_manager(self, manager):
        detections = [
            self._make_detection(
                "nmap scan",
                [{"rule": "port_scan", "severity": "MEDIUM", "description": "Port scanning detected"}],
            )
        ]
        incidents = manager.from_detections(detections)
        assert manager.get(incidents[0].id) is incidents[0]

    def test_empty_detections(self, manager):
        assert manager.from_detections([]) == []

    def test_severity_set_correctly(self, manager):
        detections = [
            self._make_detection(
                "virus detected",
                [{"rule": "malware", "severity": "CRITICAL", "description": "Malware detected"}],
            )
        ]
        incidents = manager.from_detections(detections)
        assert incidents[0].severity == Severity.CRITICAL
