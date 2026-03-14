"""Tests for autosoc.analyzer."""

import pytest
from autosoc.analyzer import LogAnalyzer


@pytest.fixture
def analyzer():
    return LogAnalyzer()


class TestParseLine:
    def test_timestamp_and_level(self, analyzer):
        line = "2024-01-15 10:30:00 ERROR Failed login attempt from 192.168.1.1"
        entry = analyzer.parse_line(line)
        assert entry["timestamp"] == "2024-01-15 10:30:00"
        assert entry["level"] == "ERROR"
        assert entry["message"] == "Failed login attempt from 192.168.1.1"
        assert entry["raw"] == line

    def test_timestamp_with_t_separator(self, analyzer):
        line = "2024-06-01T08:00:00 WARNING Disk usage high"
        entry = analyzer.parse_line(line)
        assert entry["timestamp"] == "2024-06-01T08:00:00"
        assert entry["level"] == "WARNING"
        assert entry["message"] == "Disk usage high"

    def test_bracket_level_format(self, analyzer):
        line = "[ERROR] Failed login attempt"
        entry = analyzer.parse_line(line)
        assert entry["timestamp"] == ""
        assert entry["level"] == "ERROR"
        assert entry["message"] == "Failed login attempt"
        assert entry["raw"] == line

    def test_bracket_level_with_colon(self, analyzer):
        line = "[WARNING]: High memory usage"
        entry = analyzer.parse_line(line)
        assert entry["level"] == "WARNING"
        assert entry["message"] == "High memory usage"

    def test_prefix_level_format(self, analyzer):
        line = "INFO: Service started"
        entry = analyzer.parse_line(line)
        assert entry["timestamp"] == ""
        assert entry["level"] == "INFO"
        assert entry["message"] == "Service started"

    def test_critical_level(self, analyzer):
        line = "CRITICAL: System compromise detected"
        entry = analyzer.parse_line(line)
        assert entry["level"] == "CRITICAL"

    def test_debug_level(self, analyzer):
        line = "[DEBUG] Connection pool initialized"
        entry = analyzer.parse_line(line)
        assert entry["level"] == "DEBUG"

    def test_fallback_no_level(self, analyzer):
        line = "Something happened with no level"
        entry = analyzer.parse_line(line)
        assert entry["level"] == "INFO"
        assert entry["message"] == line
        assert entry["timestamp"] == ""
        assert entry["raw"] == line

    def test_raw_field_preserved(self, analyzer):
        line = "2024-01-01 00:00:00 INFO hello world"
        entry = analyzer.parse_line(line)
        assert entry["raw"] == line

    def test_empty_line(self, analyzer):
        entry = analyzer.parse_line("")
        assert entry["level"] == "INFO"
        assert entry["message"] == ""

    def test_case_insensitive_level(self, analyzer):
        line = "2024-01-15 10:30:00 error lowercase level"
        entry = analyzer.parse_line(line)
        assert entry["level"] == "ERROR"


class TestAnalyze:
    def test_returns_list(self, analyzer):
        lines = [
            "2024-01-15 10:30:00 ERROR err1",
            "INFO: msg2",
        ]
        results = analyzer.analyze(lines)
        assert len(results) == 2
        assert results[0]["level"] == "ERROR"
        assert results[1]["level"] == "INFO"

    def test_empty_input(self, analyzer):
        assert analyzer.analyze([]) == []


class TestFilterByLevel:
    def test_filter_errors(self, analyzer):
        lines = [
            "2024-01-15 10:30:00 ERROR err",
            "INFO: ok",
            "[ERROR] another error",
        ]
        entries = analyzer.analyze(lines)
        errors = analyzer.filter_by_level(entries, "ERROR")
        assert len(errors) == 2

    def test_filter_case_insensitive(self, analyzer):
        entries = [{"level": "WARNING", "message": "w", "timestamp": "", "raw": ""}]
        result = analyzer.filter_by_level(entries, "warning")
        assert len(result) == 1

    def test_filter_no_match(self, analyzer):
        entries = [{"level": "INFO", "message": "i", "timestamp": "", "raw": ""}]
        result = analyzer.filter_by_level(entries, "DEBUG")
        assert result == []


class TestCountByLevel:
    def test_count_mixed(self, analyzer):
        lines = [
            "INFO: a",
            "INFO: b",
            "[ERROR] c",
            "2024-01-01 00:00:00 WARNING d",
        ]
        entries = analyzer.analyze(lines)
        counts = analyzer.count_by_level(entries)
        assert counts["INFO"] == 2
        assert counts["ERROR"] == 1
        assert counts["WARNING"] == 1

    def test_count_empty(self, analyzer):
        assert analyzer.count_by_level([]) == {}
