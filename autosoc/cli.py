"""CLI entry point for autosoc."""

import argparse
import sys

from autosoc import __version__
from autosoc.analyzer import LogAnalyzer
from autosoc.detector import ThreatDetector


def _cmd_analyze(args: argparse.Namespace) -> None:
    analyzer = LogAnalyzer()
    try:
        with open(args.logfile, encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError as exc:
        print(f"Error reading file: {exc}", file=sys.stderr)
        sys.exit(1)

    entries = analyzer.analyze(lines)
    counts = analyzer.count_by_level(entries)

    print(f"Analyzed {len(entries)} log entries from '{args.logfile}'")
    print("\nLevel summary:")
    for level, count in sorted(counts.items()):
        print(f"  {level:<10} {count}")


def _cmd_scan(args: argparse.Namespace) -> None:
    analyzer = LogAnalyzer()
    detector = ThreatDetector()

    try:
        with open(args.logfile, encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError as exc:
        print(f"Error reading file: {exc}", file=sys.stderr)
        sys.exit(1)

    entries = analyzer.analyze(lines)
    detections = detector.scan(entries)

    print(f"Scanned {len(entries)} log entries from '{args.logfile}'")
    print(f"Threats detected: {len(detections)}\n")

    for detection in detections:
        raw = detection["entry"].get("raw", "")
        print(f"  LOG: {raw}")
        for match in detection["matches"]:
            print(f"       [{match['severity']}] {match['rule']}: {match['description']}")
        print()


def _cmd_version(_args: argparse.Namespace) -> None:
    print(f"autosoc {__version__}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="autosoc",
        description="Automated Security Operations Center tool",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    analyze_parser = subparsers.add_parser("analyze", help="Parse a log file and print level summary")
    analyze_parser.add_argument("logfile", help="Path to the log file")
    analyze_parser.set_defaults(func=_cmd_analyze)

    scan_parser = subparsers.add_parser("scan", help="Scan a log file for threats")
    scan_parser.add_argument("logfile", help="Path to the log file")
    scan_parser.set_defaults(func=_cmd_scan)

    version_parser = subparsers.add_parser("version", help="Print version")
    version_parser.set_defaults(func=_cmd_version)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
