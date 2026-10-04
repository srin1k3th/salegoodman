"""
Seed script — populates the database with demo data via Supabase client.

Usage:
    python -m app.utils.seed

This script reads from supabase/seed.sql and executes it via the Supabase
admin client. Alternatively, you can run seed.sql directly in the Supabase
SQL Editor.
"""

import sys
from pathlib import Path


def seed_database():
    """Seed the database with demo data."""
    from app.database import supabase_admin

    if not supabase_admin:
        print("ERROR: Supabase admin client not configured. Set SUPABASE_SERVICE_KEY in .env")
        sys.exit(1)

    # Read seed SQL
    seed_path = Path(__file__).parent.parent.parent.parent / "supabase" / "seed.sql"

    if not seed_path.exists():
        print(f"ERROR: Seed file not found at {seed_path}")
        sys.exit(1)

    sql = seed_path.read_text()

    print("Seeding database with demo data...")
    print(f"Reading from: {seed_path}")

    try:
        # Execute via Supabase RPC or direct SQL
        # Note: For complex SQL, it's better to run seed.sql directly in the Supabase SQL Editor
        result = supabase_admin.rpc("exec_sql", {"sql": sql}).execute()
        print("✓ Database seeded successfully!")
        print("  - 1 workspace (Goodman & Co.)")
        print("  - 3 team members")
        print("  - 6 contacts")
        print("  - 6 leads")
        print("  - 3 deals")
        print("  - 3 escalations")
        print("  - 5 agent configs")
        print("  - 4 activity log entries")
        print("  - 4 calls")
        print("  - 3 follow-ups")
    except Exception as e:
        print(f"\nNote: If this fails, run supabase/seed.sql directly in the Supabase SQL Editor.")
        print(f"Error: {e}")


if __name__ == "__main__":
    seed_database()
