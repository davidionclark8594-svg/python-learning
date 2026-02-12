from pathlib import Path

KEYWORDS = [
    "password",
    "token",
    "sql",
    "injection",
    "xss",
    "admin",
    "secret",
    "apikey",
    "api key",
]


def scan_file(input_path: Path, report_path: Path) -> int:
    """
    Scans a file for keywords and writes a report.
    Returns number of matches found.
    """
    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        return 0

    matches = []
    lines = input_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    for i, line in enumerate(lines, start=1):
        lower = line.lower()
        for kw in KEYWORDS:
            if kw in lower:
                matches.append((i, kw, line.strip()))

    # Build report text
    report_lines = []
    report_lines.append(f"Scan report for: {input_path}")
    report_lines.append(f"Keywords: {', '.join(KEYWORDS)}")
    report_lines.append("-" * 60)

    if not matches:
        report_lines.append("✅ No matches found.")
    else:
        report_lines.append(f"⚠️ Matches found: {len(matches)}")
        report_lines.append("")
        for line_no, kw, text in matches:
            report_lines.append(f"Line {line_no:>3} | keyword='{kw}' | {text}")

    report_text = "\n".join(report_lines) + "\n"

    # Ensure report folder exists and write report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")

    # Print short summary
    print(f"✅ Done. Matches: {len(matches)}")
    print(f"📝 Report saved to: {report_path}")

    return len(matches)


def main():
    print("🔎 Simple Log Scanner")

    user_path = input("Enter file path to scan (example: Week1/sample_log.txt): ").strip()

    input_path = Path(user_path)
    report_path = Path("Week1") / "reports" / "scan_report.txt"

    scan_file(input_path, report_path)



if __name__ == "__main__":
    main()
