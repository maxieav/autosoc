"""autosoc - Automated Security Operations Center tool."""

from autosoc.analyzer import LogAnalyzer
from autosoc.detector import ThreatDetector
from autosoc.incident import IncidentManager

__version__ = "0.1.0"

__all__ = ["LogAnalyzer", "ThreatDetector", "IncidentManager", "__version__"]
