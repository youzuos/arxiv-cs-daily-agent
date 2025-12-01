"""Check if daily update is working correctly."""

import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PAPERS_FILE = BASE_DIR / "frontend" / "src" / "data" / "papers.json"


def check_daily_update():
    """Check if papers.json contains today's date."""
    if not PAPERS_FILE.exists():
        print("ERROR: papers.json not found!")
        return False
    
    today = datetime.now().strftime("%Y-%m-%d")
    data = json.loads(PAPERS_FILE.read_text(encoding="utf-8"))
    
    dates = [p["submittedAt"] for p in data]
    latest_date = max(dates)
    earliest_date = min(dates)
    today_papers = [p for p in data if p["submittedAt"] == today]
    
    print(f"Today's date: {today}")
    print(f"Total papers: {len(data)}")
    print(f"Latest date in papers: {latest_date}")
    print(f"Earliest date in papers: {earliest_date}")
    print(f"Papers with today's date: {len(today_papers)}")
    
    if today_papers:
        print("\nToday's papers:")
        for paper in today_papers:
            print(f"  - {paper['title']} ({paper['id']})")
        return True
    else:
        print(f"\nWARNING: No papers found with today's date ({today})")
        print("Run daily update to generate today's papers:")
        print("   python -c \"from backend.main import orchestrator; orchestrator.bootstrap('daily refresh'); orchestrator.run()\"")
        print("   Or: curl -X POST http://127.0.0.1:8000/update")
        return False


if __name__ == "__main__":
    check_daily_update()

