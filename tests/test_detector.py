"""Tests for autosoc.detector."""

import pytest
from autosoc.detector import Rule, ThreatDetector


def make_entry(message: str, raw: str = "") -> dict:
    return {"level": "INFO", "message": message, "timestamp": "", "raw": raw or message}


@pytest.fixture
def detector():
    return ThreatDetector()


class TestRule:
    def test_matches_true(self):
        rule = Rule("test", r"failed login", "HIGH")
        assert rule.matches("failed login attempt") is True

    def test_matches_false(self):
        rule = Rule("test", r"failed login", "HIGH")
        assert rule.matches("successful login") is False

    def test_case_insensitive(self):
        rule = Rule("test", r"failed login", "HIGH")
        assert rule.matches("FAILED LOGIN attempt") is True

    def test_description_default_empty(self):
        rule = Rule("test", r"pattern", "LOW")
        assert rule.description == ""


class TestThreatDetectorDefaults:
    def test_default_rules_loaded(self, detector):
        assert len(detector.rules) == len(ThreatDetector.DEFAULT_RULES)

    def test_custom_rules_replace_defaults(self):
        custom = [Rule("custom", r"custom_pattern", "LOW", "Custom rule")]
        d = ThreatDetector(rules=custom)
        assert len(d.rules) == 1
        assert d.rules[0].name == "custom"

    def test_none_uses_defaults(self):
        d = ThreatDetector(rules=None)
        assert len(d.rules) == len(ThreatDetector.DEFAULT_RULES)


class TestAddRule:
    def test_add_rule(self, detector):
        initial_count = len(detector.rules)
        detector.add_rule(Rule("new_rule", r"new_pattern", "LOW"))
        assert len(detector.rules) == initial_count + 1

    def test_added_rule_fires(self, detector):
        detector.add_rule(Rule("custom", r"custom_attack", "MEDIUM", "Custom attack"))
        entry = make_entry("Detected custom_attack vector")
        matches = detector.detect(entry)
        rule_names = [m["rule"] for m in matches]
        assert "custom" in rule_names


class TestDetect:
    def test_brute_force_match(self, detector):
        entry = make_entry("failed login attempt for user admin")
        matches = detector.detect(entry)
        assert any(m["rule"] == "brute_force" for m in matches)

    def test_authentication_failure(self, detector):
        entry = make_entry("authentication failure for root from 10.0.0.1")
        matches = detector.detect(entry)
        assert any(m["rule"] == "brute_force" for m in matches)

    def test_invalid_password(self, detector):
        entry = make_entry("invalid password supplied for user bob")
        matches = detector.detect(entry)
        assert any(m["rule"] == "brute_force" for m in matches)

    def test_sql_injection_select(self, detector):
        entry = make_entry("SELECT * FROM users WHERE id=1 OR 1=1")
        matches = detector.detect(entry)
        assert any(m["rule"] == "sql_injection" for m in matches)

    def test_sql_injection_comment(self, detector):
        entry = make_entry("GET /login?user=admin'-- HTTP/1.1")
        matches = detector.detect(entry)
        assert any(m["rule"] == "sql_injection" for m in matches)

    def test_port_scan_match(self, detector):
        entry = make_entry("nmap scan detected from 192.168.1.100")
        matches = detector.detect(entry)
        assert any(m["rule"] == "port_scan" for m in matches)

    def test_malware_match(self, detector):
        entry = make_entry("ransomware signature detected in file backup.exe")
        matches = detector.detect(entry)
        assert any(m["rule"] == "malware" for m in matches)

    def test_privilege_escalation_match(self, detector):
        entry = make_entry("sudo: 3 incorrect password attempts; privilege escalation blocked")
        matches = detector.detect(entry)
        assert any(m["rule"] == "privilege_escalation" for m in matches)

    def test_no_match(self, detector):
        entry = make_entry("User successfully logged in")
        matches = detector.detect(entry)
        assert matches == []

    def test_match_includes_severity_and_description(self, detector):
        entry = make_entry("failed login for admin")
        matches = detector.detect(entry)
        bf = next(m for m in matches if m["rule"] == "brute_force")
        assert bf["severity"] == "HIGH"
        assert bf["description"] == "Brute force login attempt"

    def test_detects_from_raw_field(self, detector):
        entry = {"level": "INFO", "message": "", "timestamp": "", "raw": "failed login attempt"}
        matches = detector.detect(entry)
        assert any(m["rule"] == "brute_force" for m in matches)


class TestScan:
    def test_scan_returns_only_matching(self, detector):
        entries = [
            make_entry("Normal service startup"),
            make_entry("failed login attempt for admin"),
            make_entry("All systems operational"),
            make_entry("nmap scan from external IP"),
        ]
        results = detector.scan(entries)
        assert len(results) == 2

    def test_scan_result_structure(self, detector):
        entries = [make_entry("failed login attempt")]
        results = detector.scan(entries)
        assert len(results) == 1
        assert "entry" in results[0]
        assert "matches" in results[0]
        assert len(results[0]["matches"]) >= 1

    def test_scan_empty(self, detector):
        assert detector.scan([]) == []

    def test_scan_no_threats(self, detector):
        entries = [
            make_entry("Service started"),
            make_entry("Health check passed"),
        ]
        assert detector.scan(entries) == []

    def test_scan_multiple_matches_per_entry(self, detector):
        # Entry that triggers both brute_force and privilege_escalation
        entry = make_entry("failed login: privilege escalation attempt detected")
        results = detector.scan([entry])
        assert len(results) == 1
        assert len(results[0]["matches"]) >= 2
