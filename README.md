# autosoc

**Automated Security Operations Center** — a lightweight Python tool for parsing log files, detecting threats with rule-based pattern matching, and managing security incidents.

## Features

- **Log Analysis** — parse common log formats (timestamp + level, `[LEVEL]`, `LEVEL:`) and filter/count by level
- **Threat Detection** — rule-based engine with built-in rules for brute force, SQL injection, port scanning, malware, and privilege escalation
- **Incident Management** — create, track, update, and close security incidents with severity/status filtering
- **CLI** — analyze and scan log files directly from the terminal

## Installation

```bash
pip install -e .
```

## Usage

### Python API

```python
from autosoc import LogAnalyzer, ThreatDetector, IncidentManager
from autosoc.incident import Severity

# Parse logs
analyzer = LogAnalyzer()
entries = analyzer.analyze(open("app.log").readlines())
print(analyzer.count_by_level(entries))

# Detect threats
detector = ThreatDetector()
detections = detector.scan(entries)
for d in detections:
    print(d["entry"]["raw"])
    for m in d["matches"]:
        print(f"  [{m['severity']}] {m['rule']}: {m['description']}")

# Create incidents from detections
manager = IncidentManager()
incidents = manager.from_detections(detections)
for inc in incidents:
    print(inc.to_dict())

# Manage incidents manually
inc = manager.create("Suspicious login", Severity.HIGH, description="Multiple failed logins")
manager.resolve(inc.id)
```

### CLI

```bash
# Summarize log levels
autosoc analyze /var/log/auth.log

# Scan for threats
autosoc scan /var/log/syslog

# Print version
autosoc version
```

## Running tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```
