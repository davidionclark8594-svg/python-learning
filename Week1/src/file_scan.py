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
SEVERITY_MAP={
    "password":"HIGH",
    "token":"HIGH",
    "apikey":"HIGH",
    "api_key":"HIGH",
    "secret":"HIGH",
    "xss":"HIGH",
    "sql":"MEDIUM",
    "injection":"MEDIUM",
    "admin":"LOW",
}


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
            severity = SEVERITY_MAP.get(kw, "UNKNOWN")
            matches.append((i, kw, severity, line.strip()))

                

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
    print("🔎 Directory Log Scanner")

    folder = input("Enter folder to scan (example: Week1): ").strip()
    folder_path = Path(folder)

    report_path = Path("Week1") / "reports" / "scan_report.txt"

    if not folder_path.exists() or not folder_path.is_dir():
        print(f"❌ Not a folder: {folder_path}")
        return

    total_matches = 0
    report_path.parent.mkdir(parents=True, exist_ok=True)

    # Clear old report and start fresh
    report_path.write_text(f"Scan report for folder: {folder_path}\n" + ("-" * 60) + "\n", encoding="utf-8")

    # Scan every file in the folder (recursively)
    for file_path in folder_path.rglob("*"):
        if file_path.is_file():
            matches = scan_file(file_path, report_path)
            total_matches += matches

    print(f"✅ Folder scan complete. Total matches: {total_matches}")
    print(f"📝 Combined report saved to: {report_path}")




if __name__ == "__main__":
    main()
