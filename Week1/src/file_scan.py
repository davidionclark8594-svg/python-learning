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

SEVERITY_MAP = {
    "password": "HIGH",
    "token": "HIGH",
    "apikey": "HIGH",
    "api key": "HIGH",
    "sql": "MEDIUM",
    "injection": "MEDIUM",
    "xss": "MEDIUM",
    "admin": "LOW",
    "secret": "HIGH",
}

def scan_file(input_path: Path):
    """Return a list of matches: (line_no, keyword, severity, line_text)."""
    if not input_path.exists() or not input_path.is_file():
        return []

    try:
        lines = input_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return []

    matches = []
    for line_no, line in enumerate(lines, start=1):
        lower = line.lower()
        for kw in KEYWORDS:
            if kw in lower:
                severity = SEVERITY_MAP.get(kw, "UNKNOWN")
                matches.append((line_no, kw, severity, line.strip()))
                break  # only count 1 keyword per line

    return matches

def main():
    print("🧠 Directory Log Scanner")

    # Base dir = Week1 (because this file is Week1/src/file_scan.py)
    base_dir = Path(__file__).resolve().parents[1]

    folder = input("Enter folder to scan (blank = data): ").strip()
    folder = folder if folder else "data"

    folder_path = (base_dir / folder).resolve()
    report_path = (base_dir / "Reports" / "scan_report.txt").resolve()

    if not folder_path.exists() or not folder_path.is_dir():
        print(f"❌ Not a folder: {folder_path}")
        return

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("", encoding="utf-8")  # clear report

    total_matches = 0

    for file_path in folder_path.rglob("*"):
        if not file_path.is_file():
            continue

        matches = scan_file(file_path)
        total_matches += len(matches)

        with report_path.open("a", encoding="utf-8") as f:
            f.write(f"Scan report for: {file_path}\n")
            f.write(f"Keywords: {', '.join(KEYWORDS)}\n")
            f.write("-" * 60 + "\n")

            if not matches:
                f.write("✅ No matches found.\n\n")
            else:
                f.write(f"⚠️ Matches found: {len(matches)}\n")
                for line_no, kw, severity, text in matches:
                    f.write(f"Line {line_no:>3} | {severity:<7} | {kw:<10} | {text}\n")
                f.write("\n")

    print(f"✅ Folder scan complete. Total matches: {total_matches}")
    print(f"📄 Combined report saved to: {report_path}")

if __name__ == "__main__":
    main()
